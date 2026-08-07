# Call Transcript — Kallat Properties Discovery/Demo Call

**Date: CONFIRMED 2026-07-16, 9:51am, 25 minutes.** Established via
Gmail search (`no-reply@otter.ai`, `scholarixglobal@gmail.com`) for the
Otter.ai meeting-summary notification, sent 2026-07-16 06:21 UTC,
subject "Meeting Summary for Scholarix Global's Meeting Notes," body:
*"Scholarix Global Consultant has shared notes from Scholarix Global's
Meeting Notes, Jul 16. Sadique and Johnny Gurrera discussed the need for
a user-friendly, secure, and accurate CRM system... integrate with
various property portals like Bayut and Property Finder... currently
uses Zapier for automation... AI-powered lead scoring, automatic
property posting, and client portal access for payments"* — matches this
transcript's content exactly, and the stated 25-minute duration matches
this transcript's own final timestamp (25:28). Not a file-metadata
inference (the downloaded `.txt`'s own timestamps only show the
2026-08-07 download, and were not used to date this call) — a direct,
independent, timestamped external record.

**Sequencing, now resolved**: this call is the **same morning** as
`call-transcript-2026-07-16-internal-prep.md` (that call's own three
Otter notifications run 12:47pm-1:31pm UTC the same day — afternoon,
after this one). Discovery/demo call (AM) → SGC-internal debrief (PM,
same day) → SGC-KP-2026-07 sent 7 days later (2026-07-23) → client price
pushback the next day (2026-07-24). This transcript is very likely the
actual source material SGC-KP-2026-07 was built from — its property-
management focus, portal-integration emphasis, and AI-scoring framing
all trace directly to what Sadique asks for and is shown on this call.

**Source:** Otter.ai transcript, file titled "Scholarix Global's Meeting
Notes" — this is the same Otter.ai notification subject line already
logged in `HANDOVER.md` §8.9/§8.1 in connection with **Prosper's**
2026-07-17 demo-prep call. **This transcript is not that one** — the
content below is a Kallat-specific call (Sadique Abbas, real-estate
CRM/property-portal discussion). Otter.ai evidently reused a generic
"Scholarix Global's Meeting Notes" title across multiple unrelated
recordings — the filename alone is not a reliable client identifier.

**Participants:** Sadique Abbas (Kallat Properties — client, present),
Johnny Gurrera (SGC SDR), a second SGC voice credited "Scholarix Global
Consultant" (self-identifies as having "worked in Samana before" and
implementing similar systems at "Ax Capital" — referred to once as "mr.
Brand," almost certainly an Otter.ai mis-transcription of "Mr. Bran,"
i.e. Renbran Madelo — **not confirmed, flagging the inference rather
than asserting it as fact**). **Attribution incomplete**: at 4:06-4:14
Sadique says "One more person is there," and a "Speaker 2" appears
briefly (4:11) — never named or role-identified anywhere in the
transcript. Whoever this is took no recorded speaking part beyond that
one line, but was present and unidentified for at least part of the call.

**Operational note, unrelated to pricing/scope**: demo login credentials
("Username is admin and password is admin") were spoken aloud, in full,
on this recorded call (~5:29) and are now sitting in a transcript in
this repo. Worth a line to whoever owns the demo environment
(`demo.sgctech.ai`) — not this session's call to action on, flagged for
awareness.

---

## Key exchange (headcount) — RULING: does NOT upgrade T12, stays UNSOURCED

> **Scholarix Global Consultant** [~13:04]: Okay, sir. For that, because
> you have mentioned of mostly client side and your inventory and your
> like specific targeting, right? And you want to be specified what
> really the clients needs and how? Just one more question, sir. How
> many agents do you have right now?
>
> **Sadique** [~13:28]: We have approximately 40 or 15, approximate.

**Corrected ruling, 2026-08-07 (Bran, direct instruction) — reverses this
file's own earlier framing.** An earlier pass on this file read "40 or
15" as a garbled "40 or 50" and upgraded `T12`'s provenance grade on that
basis. **That was reconstruction, not reading, and it's reverted.**
Verbatim, Sadique qualifies the number twice in one sentence
("approximately... approximate") while answering off the top of his head
in a live call — and Kallat is explicitly a **group spanning different
businesses and industries** (Sadique himself, ~11:04-11:12: "you're part
of the group, right? It's a Kallat group... different businesses across
the industry, different industry" — confirmed by him). A headcount given
informally in that context is ambiguous about *which entity* it counts,
independent of whether the number itself is 40, 50, or something else —
even a precise figure wouldn't resolve which of the Kallat Group's
businesses it describes, or whether this system is meant to size one
brokerage or several. **`USERS_NOW_PROVENANCE` in `test_pricing_engine.py`
is reverted to unverified; `users_now=40` remains UNSOURCED; T12 stays a
hard block.** See `00-intake/sdr-followup-headcount-2026-08-07.md` for
the now-two-part SDR follow-up this drives: (1) precise headcount, (2)
which Kallat Group entities would actually be on the system.

---

## Other findings from this call — see cross-references, not duplicated here

Full detail logged in `00-intake/verbal-promises.md` (verbatim quotes,
classifications), `manifest.yaml` (escalation entry), and `HANDOVER.md`
§15 (Kallat gap register + verbal-exposure summary). Index, so a reader
of this transcript alone knows where to look:

- **Per-user pricing promise** (~9:11, Johnny) — conflicts directly with
  the governed SUB-model's seat-band monthly subscription structure.
  Flagged as a **Stage 5 presentation constraint**, not a footnote — see
  `HANDOVER.md` §15 and the new decision it raises.
- **Unqualified security guarantee** (~1:48, Johnny) — "completely
  implausible" that hacking/cybercrime could occur. Absolute, unbackable,
  on the client's first-raised concern. Needs correcting in writing
  before signing.
- **Portal fee/accreditation claims** (~7:16-21:19, Consultant) —
  portal connection framed as free/one-click to the client; "already
  accredited by" Bayut/Property Finder/dubizzle — UNSOURCED anywhere in
  this repo. Conflicts with the planned Portal Sync add-on pricing
  (`phase2-catalogue.yaml`).
- **Third-party confidentiality breach** (~7:16, Consultant) — names
  another client and discloses their monthly Property Finder spend.
  Independent of this deal; candidate for `known-defects.md` as its own
  class (flagged for the Commercial Desk — `00-knowledge/` is read-only
  to this agent).
- **Demoed-but-unpriceable features**: AI lead-probability scoring
  (already priced as an add-on, `ai_lead_scorer_lite`), agent commission
  calculation (no `hour-lookup.yaml` entry, same gap as Prosper), auto-
  reconciliation of client/landlord payments (no catalogue entry at all),
  client/landlord portals (no catalogue entry), live-synced website
  module (a *different* feature from the catalogue's
  `website_lead_capture`, which is a lead-capture widget, not a full
  synced site). Full gap register in `HANDOVER.md` §15.
- **Scope signal**: Sadique's own redirect (~18:55) names "property
  management" and portal integration as his actual priority —
  `client-brief.yaml`'s `work_packages_requested` list doesn't contain
  either as named items. Separately, incumbent system (Zapier + Google
  Sheets) *is* already correctly recorded in `client-brief.yaml` — not a
  gap, confirmed by re-reading the file directly.
- **Odoo named to the client** ("this is Udo platform," ~20:39) — checked
  against `00-knowledge/clause-library/edition-and-upgrades.md`, which
  itself models "Your platform is built on Odoo..." as approved
  disclosure language. **Not a violation** — naming the base platform is
  expected; only naming the *edition* (Community vs Enterprise) unasked
  is the actual constraint, and that wasn't crossed here.

---

## Full transcript (verbatim, as supplied)

Sadique  0:00
For example, so while while we have this this all the the details, we just need to be in in in taking place one one area to be organized to have everything has to be systematic, right? So we need to have the system to understand. No, we don't want to have like you know very complicated system. We need to have the system which is, as I said, it's a friendly user. And the same time, at the end of the day, everything is has to be in in have accountability. So this is what we are looking as a real estate. We are receiving plenty of leads, and also in I don't know how the secure the system is when it comes of is a confidential details, especially the data client details and everything. How well known you are in the market and how you can even someone is breaching the security or data, how you well protected, because the AI is taking over right now, so we have to make sure that everything will be very confidential, and especially when it comes client details, another details has to be you know in in well secured. So we in all over what I need to say that we need to have the system which is very accurate. Accurate and friendly user, and we need to to arrange everything in that system. Especially, for example, if I'm assigning to some leads to one agent or particular agent, has to be goes to the same exactly the agent without any you know disk frequency. or whatever it is. So this is what we are looking

Johnny Gurrera  1:48
for. Understand well. Like I said, the UI is very simple. It's all just a bunch of seeing and clicking. And I already told you the Udo that we have can integrate into any portal and grant you easy accessibility. You need efficiency, and what you currently have with your employees using Google Sheets or other systems, it requires them having to input all their data and then file their reports and then give it to you separately. This could take days. Right over here, they could just log what they need immediately into this one system, and it would be in their profile. You know, all perfectly organized. You aren't lacking in anything. And as far as security goes, our system is already bolstering and making sure that any cyber crimes or hacking, it remains completely implausible. I mean, we know how important security is, and we know how AI is always trying to is always being utilized for cyber crimes and breaching security. And I promise, assure you, sir, we're doing our best to get around that. Everything that you're saying, everything that you're saying is all comes down to you needing one unifying system, and we have that right here. We just need to build it around your company's needs. All the data that you have, we can back end it and upload it. Everything that you need organized into bar by bar that's accessible for everyone and easily, we can get that built. The only thing that we need is you're okay to go ahead with it.

Sadique  3:36
So who is joined? Can I have maybe Facebook?

Johnny Gurrera  3:39
My my manager

Scholarix Global Consultant  3:42
is hi, mr. Abak. Good morning.

Sadique  3:45
Good, good. How are you? Can you just we want to see everyone so that we will have transferred and somehow hi.

Scholarix Global Consultant  3:51
How are you?

Sadique  3:55
Very good. Yeah, thank you.

Scholarix Global Consultant  3:56
Yeah, yeah. How about you? How was everything?

Sadique  4:01
Everything is okay. Everything is good.

Speaker 1  4:02
So doing

Scholarix Global Consultant  4:04
well. All right, sir. All

Johnny Gurrera  4:05
right.

Sadique  4:06
One more person is there.

Scholarix Global Consultant  4:08
I'm not taking AI.

Speaker 2  4:11
Oh, okay.

Sadique  4:14
Yes, please. Yeah.

Scholarix Global Consultant  4:19
Then I think you can you can show mr. Abbas the the demo lag in credentials that we have because I think it will be more specifically to their needs rather than this kind of things. I I guess so you have projects right in the Tilal community.

Sadique  4:42
Yeah. Yes. Yeah.

Scholarix Global Consultant  4:45
So basically, we have end-to-end project property management from off-plan projects to rental and maintenance. So it's an end-to-end module that you don't need to have anything because everything is here and unified. So I guess most because what John said to me that you have looking for unified system. Then admin admin John just email email is admin. Admin. Yeah. Username is admin and password is admin.

Johnny Gurrera  5:29
Okay.

Scholarix Global Consultant  5:40
So now, yes, this is our

Johnny Gurrera  5:42
here. Here's a prop. Here is the property management demo. This

Scholarix Global Consultant  5:46
one is our property management, mr. Avas. So from, I know that you have an inventory of projects, properties. So if we will navigate to properties, you can click properties, John. Property. properties no no in the menu in the side properties

Johnny Gurrera  6:07
total properties

Scholarix Global Consultant  6:08
yeah so here you can show him sample of properties open it open one yeah I got

Johnny Gurrera  6:18
I got one I'm choosing good one yeah over here Dubai Towers Unit 209 I look at all the information that's perfectly here, all spaced apart, also in a white screen, so there's no confusion.

Scholarix Global Consultant  6:30
Yeah. So also, sir, mr. Abbas, this one is able to post in one go. For example, you have listed this property, and in just one go, you can post it in different portals, property portals, using their APIs. So, if you have, if you want to list it in multiple at once, it can be done. So, you don't need to log into each of property portal because everything is already set up. You just need the API keys of this property portal. That's it. One click.

Sadique  7:07
Sorry, one question. API. Do you have access of API? How are you aligned with those portal by you to Bizzle? Are you actually?

Scholarix Global Consultant  7:16
Yeah. Yes. The answer is that is that their API is not free? We can we can have their API, but there there have a fees involved in their API key. So I think if you will want to register in what one my one of my client Oses properties they register in the API keys, they I think they paid monthly for around 30,000 dirhams for property finder.

Sadique  7:48
But API usually see for example because I have an experience, so the the most of the company like you know the integrated company CRM company already have tie up with those property finder by youth and do business to to integrate because if, for example, if I'm sending the email to the property finder by youth and do business asking for API key, then they check your background if they are well known or you know the yeah yeah then they definitely they say yeah you can do it without any charges so that means the post will go

Scholarix Global Consultant  8:22
there. Yes, that will be simplified because if you have already tied up with this property portal, then if they are giving us the API key, just one click, it will be connected. So every time you will want to post or remove the listing, then it will be easy as that. One click, one click only. And for that, we have multiple types of property portal that we can able to connect. We just need their endpoints, so there's no issue about that because we have already done this with multiple real estate. If you familiar with Ax Capital, also I was working in Samana before, and we also implement this kind of system.

Johnny Gurrera  9:11
There's something I also want to chime in. When it comes to conventional CRM systems, they always have you on a high monthly budget where they allow you to pay by the users that work that are use their system like five to 1010, to 1515, 20 etc. They're always squeezing you for money on a monthly basis, and then when you need additional features of their software to run whatever specific tasks you have, they ask you for even more money. You're just hemorrhaging more from your budget. Our system, when you pay for it, when when you when you get it, you have everything at your disposal. It's just an additional benefit that I wanted to inform you of, sir. You have everything right from the get go. No, it's that straightforward. When we made it, we designed it to be straightforward and convenient in every single sense of the way. That's how mr. Brand wanted it. That's how we're taught to understand it. That's how it functions, and that's how we're informing you of it, as we continue showing it to you. Straightforward A to B, no difficulties, just non-stop efficiency and business growth because of it. We provide you with the tools that you have. That's what we give you the solutions.

Scholarix Global Consultant  10:49
mr. Abbas, can I ask you once one question?

Sadique  10:54
Yeah.

Scholarix Global Consultant  10:54
Just want to understand your business operation because I think you're part of the group, right? It's a caliat group, right?

Sadique  11:04
Yeah. And you have

Scholarix Global Consultant  11:05
different businesses across the industry, different industry.

Sadique  11:11
Yeah.

Scholarix Global Consultant  11:12
And right now, actually, what you really needs to needs from us so that we can able to provide you more significant demo for your needs because so we can address the main concern that you are having now. At least we can solve the problem.

Sadique  11:35
Main as already I informed Johnny that we are looking for CRM which has to be integrated with all the property finder, Meta, Google, and website whatsoever, and also we need to have the system central system as CRM. And I don't know what other past website and everything will be cleaned up. And look at the website and see the advice or consultant do the consultancy how it's going to be a you know to to to make better as in the future. So as we are the group group of company. So this is all what we are looking for, especially the CRM and plus website or the social media has to be you know well known and to be well, I mean, to get the captivation from the audience, so the right audience, the right target, we have to do it. So now it is not that exactly what we are player keep in placing because it's it's it's a completely different perspective, which is client. If, for example, one client is looking for one apartment or bedroom or whatever it is, so they get confused again looking at the website. We have to have the client when we are looking the client. So you know the especially the SEO whatsoever should be accurate. Should be well maintained. This is what we are looking.

Scholarix Global Consultant  13:04
Okay, sir. For that, because you have mentioned of mostly client side and your inventory and your like specific targeting, right? And you want to be specified what really the clients needs and how? Just one more question, sir. How many agents do you have right now?

Sadique  13:28
We have approximately 40 or 15, approximate.

Scholarix Global Consultant  13:33
Okay, so how they are doing their CRM now? What CRMB they are using?

Sadique  13:40
We are using. I I told him already. We are using the Zapier, and most of them we are doing that. Ah, okay.

Scholarix Global Consultant  13:46
Ah, you doing automation? Ah, yeah. Zapier automation. Ah, okay.

Sadique  13:51
Yeah,

Scholarix Global Consultant  13:52
that's good. So, ah, for the listing, ah, how about our agent? For example, you have ah for listing ah the properties. So the your admin is doing it right now manually, log into the portal and then post the property that for listing. Is that correct?

Johnny Gurrera  14:10
That's what I told you about, sir. Yeah, yeah. So time consuming.

Scholarix Global Consultant  14:15
So so for that, definitely we can address multiple challenges that you are facing in just one one app or one modules, because from here the posting posting is will be very simple, and also there is also a leads. You can click John in your menu. There is a menu tab that leads the name beside of regions. No, the John in the nub here only in the property leads. The name of leads. Upper upper in the nav bar.

Johnny Gurrera  14:50
Oh wait, I see it. I see it. In the dash dashboard, sir. Yeah, leads. So

Scholarix Global Consultant  14:56
from here, we can able to assess the leads because we have here AI powered also, so based on the information from your leads generation form, you can able to calculate the probability of closing the closing the client because you will the AI will gather information based on the form that was submitted. So he will also dig more in whatever is available in the internet, and then he will give you a percentage of the probability of closing the client. So you can now assess which client or which leads your agent will focus. Other than low scoring leads, it will you will be now able to see. Okay, I will prioritize this one because this is 85% of probability. High probability means you will be focused on that. So lower probability, you can do it on your free, so this is how our leads CRM works, and also we can have specific things that we can put on the tabs. There's no issue as per your company policy for leads distribution, leads handling, because

Johnny Gurrera  16:20
look, mr. Some

Scholarix Global Consultant  16:23
of our agencies, you give links, but they will not immediately call the client. That's I think that's most basically is facing the challenge.

Johnny Gurrera  16:36
Look, mr. Abbas, may I give you my personal opinion? While we've been having this meeting, you've prioritized very cleverly how you want your customers to see your business. You've talked about your your front. You've talked about your reputation, the appearance, how you want them to see your properties, how you want them to direct. What we're basically offering you is something that, while not necessarily applicable, not in its entirety and the way you want to the front end of your business, is most certainly invaluable in the back end, in the operations and how your employees work together. If you understand what I mean, that's what we're helping you address, right? When it comes to advertising and displaying and your properties, listings, and everything, that's good. That's important. You want to. You want the captivating appearance. You want customers to come, but you also a good computer's front end can only work if it's backend works just as well and perfectly so. That's what we're giving you tools with your operations management and your data management would absolutely skyrocket with our modules.

Sadique  17:57
Yeah. So Johnny and sorry, can I tell you? So,

Johnny Gurrera  18:00
can

Sadique  18:01
you just what you can do? Can you just give the proposal what I have give you, and we can sit one more meeting maybe after like after you concluding this proposals. All right, because I do step another meeting as well.

Scholarix Global Consultant  18:17
Yeah, yeah, sure, sure, sure, mr. Abbas. So I so anything questions for our for what we have discussed overall anything new? Yeah, you

Johnny Gurrera  18:29
told me about what you needed. What about now post this meeting? What specifically cropped up?

Sadique  18:38
Sorry, I didn't get you.

Johnny Gurrera  18:41
You told me about what your company needs. I understand that, but after this meeting, what specifically crops up, like comes up, and you need most addressed that you don't see. No, this is

Sadique  18:55
the one. The yeah, yeah, the property listing. The what we I didn't I didn't understand that you were doing a you know, good in the property where you are addressing. So you are more focusing also this thing. So this is something which is, we could see it, we could get the attention on this. So this is something we are interested. So let me have the proposal on the the one which you are open property management. That is something which is you know with is aligning the what we are looking for. So, if that only challenge, as I said, if is when it comes API or the credentials to to you know the connect with other party, third party. Let's say the youth do business portal portals, which is to be integrated to to collaborate with them. So that is a challenge just now because you said you can't have direct access or API key without paying. So as he said, we need to have a good relation with, or if we need to send the email to get the API. That is doesn't work like that because yeah

Scholarix Global Consultant  20:03
yes yes. Once you have have the API, then that's very great.

Sadique  20:07
No, no, no. We have this is how design. Yeah, yeah.

Scholarix Global Consultant  20:09
So there's no issues, sir. If you have API, then there's no payment about involved because it's their part. So if you have the API, we just paste the API here, post it on the portal.

Sadique  20:21
No, this this is the question what I'm asking. APA is okay. They will give because we are already paying, and they are.

Scholarix Global Consultant  20:28
Yes, and yes,

Johnny Gurrera  20:29
we can just put it in here.

Sadique  20:31
Yeah, but when it comes your part, because they also will check is they are eligible for to give the APA. Is that well known? Ah, yes, sir.

Scholarix Global Consultant  20:39
Yes, I can I can answer now right right now because yes if you have the API we can connect because our our software is already accredited by them this is Udo platform so we don't we don't have any reengineered the system so we just make it more usable on the specific industry, and that's it. This is udoo.com. You can search the the system itself. So it's really ah good for these platforms. Bayut property find the the bezel. This is already been addressed.

Johnny Gurrera  21:19
That's no such setback. That's no such. Okay, no

Sadique  21:22
worries. Now I understand what you can do. So based on this input that we have discussed, just give me the proposal and let me go through it and including the pricing to discuss it.

Scholarix Global Consultant  21:31
You can you can show mr. Abbas also just the website because we have also property listing in our website. You can go to menu and then go to website. Website.

Johnny Gurrera  21:46
I'm looking for it. Here it is. Okay, I don't want to miss it.

Scholarix Global Consultant  21:54
Website. See, this is how it looks. If you have a this module because it's included the front end with the design it properly, just and then you can click view details. Click John.

Johnny Gurrera  22:09
Yeah, I got this one. I really love village design like this.

Scholarix Global Consultant  22:13
They can put the inquiry here. Yeah, and then it's very user friendly also, then they will fill up the details. The good thing that we set here is when the client when the client will fill up the fields, they can able to grade to get the brochure automatically or the specifics of the properties in PDF file.

Sadique  22:39
Okay, let me ask you. So this is how do do it? Does it fetch into the website? Is it once you upload in the CRM, it fetch into website and or yes sir, it automatically fetch?

Scholarix Global Consultant  22:51
Yes, yes, directly sir, live. It's interesting.

Sadique  22:57
What about if if I'm gonna remove if the soldier? Yeah, it will

Scholarix Global Consultant  23:02
also sir.

Johnny Gurrera  23:03
Yeah, it's technologically symbiotic. Think of it that way, and synergetic in that symbiosis. We have

Scholarix Global Consultant  23:12
additional feature for this. For example, you have clients that especially have off-plan installment plans. We can also give portal access for the clients, and for if you are also doing rental, we can also give them. And if you have landlords like that, we can have the portal, and they can see their dashboards. They can pay online, they can pay. They can pay directly in the system, without you, without your accountant having a headache for doing the reconciliation because it will be auto reconciled. And also from here, our commission calculation for the agents as as very streamlined. You just need to put their percentage, how much they are getting, and that's it. It will just automatically calculate because

Johnny Gurrera  24:09
we offer convenience. Sure. There, there's

Scholarix Global Consultant  24:12
a. If you want, sir, we can give you also an access for meantime for this our portal. This is our demo website, demo database. You can play around with it, and then you can see if your problem will be addressed in our system. So at least you are confidently say that okay, we can how we can move forward, how we can do it, because we just want our really goal is to address specific of your current challenge. This is our goal. So right now it's up to you. We will send you our proposal as per your request and just just have it try in our portal. John will give you the access and end it.

Sadique  25:04
Okay, so I don't want to take much time now. So because yes, sir, yes, sir,

Scholarix Global Consultant  25:10
yes. Thank you, sir. Yeah, I only have three

Johnny Gurrera  25:12
minutes left. So okay, sir.

Scholarix Global Consultant  25:15
So when we will book our next meeting?

Sadique  25:19
Ah, no worries. Let me go through it. I need some time. Maybe end of this week or by Monday is okay. Monday or Tuesday?

Scholarix Global Consultant  25:25
No problem, sir. Thank you, mr. Abar.

Sadique  25:28
Yeah. Have a nice day. Have a nice day. Enjoy. Yeah. Sure. Thank you very much. Yeah. Just.

Transcribed by https://otter.ai
