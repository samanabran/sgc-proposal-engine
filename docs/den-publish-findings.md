# Den publish findings — read this before touching `release` again

Written 2026-08-04, on branch `fix/den-rest-api-publish`, after a full round-trip
through a nonexistent CLI, a verified-but-unusable REST endpoint, and the
connector path that's the actual way forward. If you're picking this up cold,
start here — every claim below is sourced against the OpenWork monorepo
(`ee/apps/den-api`, `ee/apps/den-web`) as it existed at the time of writing, not
against the public docs (which partially 404 and were partially wrong about
auth).

## 1. The phantom `den` CLI

The original `release` job ran `den marketplace publish --name ... --plugin ...
--token "$DEN_TOKEN"`. No `den` CLI is publicly distributed. Pushing a real tag
against this step failed with `den: command not found` (exit 127) — confirmed
by actually pushing a tag and watching the run, not by inspection. There was
never a fallback path or a hidden install step; it was written against a
command that doesn't exist.

**Do not reintroduce a `den` CLI invocation.** The `workflow-integrity` gate in
`.github/workflows/plugin-gates.yml` fails the build if a bare `den
<subcommand>` pattern reappears in either workflow copy.

## 2. `import-mcps-from-github-url` — verified real, but only for public repos

### The route exists

- Handler: `ee/apps/den-api/src/routes/org/plugin-system/routes.ts:941-976`
  (`POST`, registered via `withPluginArchOrgContext`).
- Path: `ee/apps/den-api/src/routes/org/plugin-system/contracts.ts:138,171` —
  `orgBasePath = "/v1"`, path is
  `${orgBasePath}/plugins/import-mcps-from-github-url`. The web app proxies
  `/api/den/*` to this at `ee/apps/den-web/app/api/den/[...path]/route.ts` via
  `ee/apps/den-web/app/api/_lib/upstream-proxy.ts` (forwards `Authorization`
  and `x-api-key` headers verbatim; strips only hop-by-hop / spoofable
  headers).
- Preview variant: same file, path
  `${orgBasePath}/plugins/import-mcps-from-github-url/preview`
  (`contracts.ts:170`).

### Request body — every field confirmed real

`ee/apps/den-api/src/routes/org/plugin-system/schemas.ts:408-422`:

```ts
export const githubPluginMcpImportPreviewSchema = z.object({
  githubUrl: z.string().trim().url().max(2048),
})

export const githubPluginMcpImportSchema = githubPluginMcpImportPreviewSchema.extend({
  access: githubPluginMcpImportAccessSchema.optional(),
  authType: z.enum(["oauth", "none"]).optional().default("oauth"),
  credentialMode: z.enum(["shared", "per_member"]).optional().default("per_member"),
  description: z.string().trim().max(65535).nullable().optional(),
  marketplaceId: marketplaceIdSchema.optional(),
  name: z.string().trim().min(1).max(255).optional(),
  selectedSkillKeys: z.array(z.string().trim().min(1).max(1024)).max(200).optional(),
  selectedServerKeys: z.array(z.string().trim().min(1).max(1024)).max(200).optional(),
  selectedServerNames: z.array(z.string().trim().min(1).max(255)).max(200).optional(),
})
```

- `githubUrl` is the only required field.
- `selectedServerNames` **is real** — flagged as suspect during review because
  it's absent from the *preview* response schema, but it's a legitimate
  request field, destructured at `routes.ts:971` and consumed at
  `store.ts:4596,4599-4600` as an alternate to `selectedServerKeys` for
  matching servers by name instead of key. Not invented.

### Defaults verified from `importGithubPluginMcps`, `store.ts:4577-4766`

- `access` omitted → **defaults to `{ orgWide: true, memberIds: [], teamIds: [] }`**
  (`store.ts:4611-4615`). This is why the release job never selects
  `sgc-commercial-desk` skills automatically — there is no known Den member ID
  to scope access to the approver instead, and the desk plugin's skills
  (margin floor, cost-to-serve, concession-ladder true values) must never
  default to org-wide.
- `marketplaceId` omitted → `attachPluginToMarketplace()` is only called if
  truthy (`store.ts:4730-4737`); omitting it creates a **standalone plugin**,
  not a marketplace entry, and the response's `marketplaceId` comes back
  `null` (`store.ts:4747`).
- `name` omitted → falls back to `importedPluginName(plan)` (`store.ts:4624`).
- The import response has **no top-level `.warnings` field** (unlike
  preview) — `store.ts:4744-4751` returns exactly `{imported, importedSkills,
  marketplaceId, plugin, skipped, skippedSkills}`. Any validation script must
  check `.skipped` / `.skippedSkills` instead.
- No documented idempotency contract for re-imports; a repeat call creates a
  second, separate plugin.

### Auth — corrected mid-investigation, then empirically confirmed

`ee/apps/den-api/src/auth.ts:1150-1169` registers Better Auth's official
`apiKey()` plugin: `defaultPrefix: "den_"` (matches `DEN_TOKEN`'s prefix
exactly) and `enableSessionForAPIKeys: true`. `ee/apps/den-api/src/session.ts:229-257`
(`getRequestSession`) tries Better Auth's own `auth.api.getSession()` **first**
— which, with the apiKey plugin registered this way, resolves an `x-api-key`
header to a full session at that step — before the separate manual
`Authorization: Bearer <token>` fallback (`session.ts:131-217`, which looks
the token up directly against the session table — i.e. a genuine
browser/app session token, not an API key) is ever reached.

**`x-api-key` is the primary scheme for a `den_`-prefixed token; `Authorization:
Bearer` is the fallback**, opposite of what the public docs page implied (it
listed Bearer for `create`/import without mentioning `x-api-key` as an
alternative there, unlike the `preview` doc page). Confirmed empirically: a
real CI run's preview call using `x-api-key` got HTTP 404, not 401/403 — it
authenticated cleanly and failed for an unrelated reason (see next section).

### Why it still can't be used: public-repo-only, and this repo is private

`samanabran/sgc-proposal-engine` **is private**
(`gh repo view ... --json visibility` → `"PRIVATE"`, and confirmed by design —
the repo carries client PII, pricing/margin data, and MSA contract terms in
history, which is exactly why private was chosen deliberately over public
when the repo was created).

`computeGithubPluginMcpImportPlan` (`store.ts:3759`) calls
`getPublicGithubRepositoryTree` → `requestPublicGithubJson`
(`store.ts:416-423`), which does:

```ts
const response = await fetch(`https://api.github.com${input.path}`, {
  headers: { Accept: "...", "User-Agent": "openwork-den-api", "X-GitHub-Api-Version": "..." },
  // no Authorization header at all
})
```

No token, ever. `store.ts:451-453` has a friendlier error for this case
(`private_github_repo`, 400, "Private GitHub repositories must be imported
through the GitHub connector") — but that branch is **effectively
unreachable** for a repo this account has no access to: GitHub's own API
returns a bare `404` to unauthenticated requests for private repos (by
design, to avoid leaking repo existence), so the request fails before the
code ever sees `private: true` in a response body. That 404 is exactly what a
real run against `citest-2026-08-04-2` produced.

**Conclusion, stated plainly: the URL-import path was never viable for this
repo.** Not "not a great fit" — categorically impossible while the repo stays
private, regardless of `DEN_TOKEN`, regardless of auth scheme. The connector
is not an upgrade path; it is the only path.

## 3. The GitHub connector — the real path, not yet provisioned

None of the required env vars exist on `den-api` today (checked via `vercel
env ls` against the live Vercel project — only
`DEN_BETTER_AUTH_TRUSTED_ORIGINS`, `DEN_DB_ENCRYPTION_KEY`,
`BETTER_AUTH_SECRET`, `DATABASE_URL`, etc. are set; no `GITHUB_CONNECTOR_*`).
Calling `startGithubConnectorInstall` today 409s with
`github_connector_app_not_configured` (`store.ts:3469-3477`,
`github-app.ts:105-121`).

### Required env vars (`ee/apps/den-api/src/env.ts:452-458`)

```
GITHUB_CONNECTOR_APP_ID
GITHUB_CONNECTOR_APP_CLIENT_ID
GITHUB_CONNECTOR_APP_CLIENT_SECRET
GITHUB_CONNECTOR_APP_PRIVATE_KEY
GITHUB_CONNECTOR_APP_WEBHOOK_SECRET
```

### GitHub App permission checklist (derived from every API call in
`ee/apps/den-api/src/routes/org/plugin-system/github-app.ts`)

- **Repository permissions**
  - **Contents: Read-only.** Every content-reading call needs it: file
    contents (`.../contents/...`, lines 412, 435, 469, 475) — including the
    `.claude-plugin/marketplace.json` / `plugin.json` manifest detection —
    commits (`.../commits/{branch}`, lines 556, 593), git trees
    (`.../git/trees/{sha}`, line 613), and branches
    (`.../branches/{branch}`, line 711). GitHub's REST API maps all of these
    to the Contents permission.
  - **Metadata: Read-only.** Required by GitHub for every App regardless;
    also directly exercised by the repo-info call (`.../repos/{owner}/{repo}`,
    line 673) used to validate installation targets.
  - **Nothing else, and nothing write.** Every call in `github-app.ts` is a
    `GET`, except the two `POST`s to GitHub's own App-auth endpoints
    (`/app/installations/{id}/access_tokens`) which aren't repository
    permissions at all — they're how the App exchanges its JWT for an
    installation token.
- **Organization permissions: none.** No call anywhere in `github-app.ts`
  touches `/org/...` or `/orgs/...`.
- **Webhook events to subscribe to** (exact accepted set, from
  `ee/apps/den-api/src/routes/webhooks/github.ts:67` and
  `store.ts:6136`): `push`, `installation`, `installation_repositories`,
  `repository`. Only `push` (sync trigger) and `installation` with
  `action: "deleted"` (marks the connector account disconnected,
  `store.ts:6154-6161`) currently do anything; the other two are accepted by
  the type but currently no-op (`store.ts:6153-6163`, falls through to
  `"event ignored"`). Subscribe to all four anyway, since the receiver
  already recognizes them and a future change may activate them without a
  webhook resubscription.
- **`GITHUB_CONNECTOR_APP_WEBHOOK_SECRET` is genuinely exercised, not just
  required to boot.** `ee/apps/den-api/src/routes/webhooks/github.ts:45-59`
  verifies `x-hub-signature-256` via HMAC-SHA256 against the raw body on
  every delivery; without the secret configured the ingress route 503s
  outright (line 46-48).
- **Public vs. private App: no constraint from Den's code either way** — this
  is a GitHub Apps platform setting you choose at creation time
  ("Only on this account" is fine), unrelated to anything in this codebase.

### Private key format — code accepts either, pick the Vercel-safe one

`ee/apps/den-api/src/routes/org/plugin-system/github-app.ts:101-103`:

```ts
export function normalizeGithubPrivateKey(privateKey: string) {
  return privateKey.includes("\\n") ? privateKey.replace(/\\n/g, "\n") : privateKey
}
```

It auto-detects: a raw multiline PEM (real newlines, no literal `\n`) passes
through unchanged; a single-line PEM with literal `\n` escape sequences gets
converted back to real newlines before use in `createGithubAppJwt`
(`github-app.ts:191-205`, Node's `crypto.createSign("RSA-SHA256").sign(...)`).

**For Vercel specifically, use the single-line `\n`-escaped form** — it's the
format the multiline-env-var problem the code was clearly written to
tolerate, and it's far less likely to get mangled by a paste into Vercel's
CLI or dashboard than a real multiline value. Convert the downloaded `.pem`:

```bash
awk '{printf "%s\\n", $0}' downloaded-key.pem
```

This prints every line followed by a literal `\n`, all on one output line,
including a trailing `\n` after the last line (harmless — PEM parsers expect
a trailing newline anyway). Copy that single line as the env var value.

### `vercel env add` commands (placeholders — run these yourself, values never
handled by the agent)

```bash
vercel env add GITHUB_CONNECTOR_APP_ID production
vercel env add GITHUB_CONNECTOR_APP_CLIENT_ID production
vercel env add GITHUB_CONNECTOR_APP_CLIENT_SECRET production
vercel env add GITHUB_CONNECTOR_APP_PRIVATE_KEY production
vercel env add GITHUB_CONNECTOR_APP_WEBHOOK_SECRET production
```

Run from a directory linked to the `den-api` Vercel project (see the earlier
`vercel link --scope renbrans-projects --project den-api` pattern used
elsewhere this session). Each command prompts interactively for the value —
paste the private key as the single-line `\n`-escaped string from above.
**A new deployment is required** for Vercel serverless functions to pick up
env var changes — this is standard Vercel platform behavior, not something
particular to this code; existing running deployments do not hot-reload env
vars. Redeploy (`vercel --prod` or push a commit that triggers one) after
setting all five.

### Provisioning sequence, start to finish

1. Create the GitHub App on GitHub (you, not the agent) — permissions and
   webhook events per the checklist above.
2. Set the five env vars on `den-api` via `vercel env add` (you, not the
   agent) — private key in the `\n`-escaped single-line form.
3. Redeploy `den-api`.
4. Run the interactive install flow: `startGithubConnectorInstall` → visit
   the returned `redirectUrl` (GitHub's own install page) → grant access to
   just `samanabran/sgc-proposal-engine` → GitHub redirects back with an
   `installationId` → `completeGithubConnectorInstall`.
5. Set up the connector instance/target pointing at the repo+branch —
   `githubSetup` (`routes.ts` "GitHub" tag, creates account + instance +
   target + initial mappings in one call) or the discovery+apply pair
   (`getGithubConnectorDiscovery` / `applyGithubConnectorDiscovery`).
6. Only then rewrite the `release` job's publish step against the connector
   API. Materially different shape from what's on this branch today:
   `applyGithubConnectorDiscovery` selects by **plugin key**
   (`selectedKeys`, matching `discoveredPlugins[].key`), not by individual
   skill key — and unlike direct import, it auto-creates and attaches to a
   marketplace when the source classifies as `claude_marketplace_repo`
   (`store.ts:5864-5874`), which is actually a better structural fit for our
   two-plugin repo than the flat skill-key list this branch's script builds.
   **The skill-derivation jq logic on this branch will not be reused as-is.**

## What's on `fix/den-rest-api-publish` right now

The `release` job still calls the direct `import-mcps-from-github-url`
endpoint. It is fully verified (route, schema, auth, response validation) and
will run cleanly against a **public** repo — but will always 404 against
this private one until the connector replaces it. Left as-is deliberately:
it fails loudly and specifically, not silently, and documents exactly what
it's blocked on. Do not try to make it succeed by tweaking `DEN_TOKEN` or the
auth header again — that's not the blocker.
