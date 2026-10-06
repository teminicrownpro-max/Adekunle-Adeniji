# QA list: Scenarios 1 and 2

Team Dart | PRISM Request | MDPM 883 Assignment 3 | Working session, Monday 5 October 2026

**Basis:** meeting record, Guiding Scenario, Milestone 1 research, Revision 2 of the Requirements Document, and the prototype screen text pasted on 5 October. The live Figma file could not be opened, so every item still needs an on-screen check.

**Evidence tags:** C Confirmed (two or more independent sources) · S Single source · H Hypothesis (team design answer, unseen by users) · A Assumption (no source) · TD / TS Team decision or team source (not user evidence) · N/A internal consistency.

**Priority:** P1 before the link goes to Cohen · P2 before usability testing · P3 recorded now.

**Totals:** 33 items (12 Scenario 1, 12 Scenario 2, 9 across both). 16 P1, 15 P2, 2 P3.

## Scenario 1: creating and submitting a furniture request

- **1.1 Home: My work orders [P2]**
  - **Issue:** Inconsistent. The earlier demonstration opened on a work order list in the Figma file and on a dashboard in the HTML reference; the default was left “to be tested”. The pasted earlier screens open on “My Work Orders”, a list with a Draft row. The 3 October brief specifies a Dashboard plus a separate My Requests list.
  - **Evidence status:** **H.** Team preference is split. No user has seen either layout.
  - **Validation needed:** Usability test, Q1 and Q2.
  - **Recommended change:** Treat as resolved by the brief once the new build is seen to open on the Dashboard. If it does not, keep one list with a visible Draft status and a “Needs your attention” marker on each row.
- **1.2 Before you start: request type [P1]**
  - **Issue:** Inconsistent. In the earlier build request type is step 3 of 6, after “Before you start” and “Client checklist”. The 3 October decision puts it first; whether the new build does so is not verified. The earlier build’s second option, “Another request type — options to be confirmed”, is selectable.
  - **Evidence status:** **TD** (3 Oct). **S:** the checklist applies only to furniture requests (PM-side interview, as reported by Felix).
  - **Validation needed:** Type names against the Requirements Document, confirmed with Cohen (O1).
  - **Recommended change:** Make request type the first choice. Show Furniture and the three [PM] categories described in the brief, and mark post-submission rules for the [PM] categories as unverified.
- **1.3 Checklist step (download and “I reviewed”) [P1]**
  - **Issue:** Duplicated. The step repeats the legacy download-and-confirm pattern and duplicates the review page. Removal was agreed, then contested; the step was still in the file. The Help page meant to hold the full checklist does not exist.
  - **Evidence status:** **S:** Kai’s difficulty was finding what the checklist asks for. Removal is **TD**. **A:** that a signed-off checklist is a mandatory record.
  - **Validation needed:** Anne-Marie today (what did she want kept, C3). Cohen: attested, attached or guidance only?
  - **Recommended change:** Remove the step. Build a Help page with the full checklist and download, reachable from every step. Add one tick on the review page only if Cohen says attestation is mandatory.
- **1.4 Side-panel checklist [P1]**
  - **Issue:** Missing. The earlier build shows only a static “Request checklist summary” (request type, location, furniture need, supporting files). The brief asks for an expandable helper. The earlier claim that automatic ticking and pop-ups cannot run in a manually linked Figma build was not checked and may not apply to the Make build.
  - **Evidence status:** **H** for the panel. **A** for the coordinator’s use of the ticks.
  - **Validation needed:** Teaching team’s reply on build method (A1). Usability test.
  - **Recommended change:** Build the helper as a reference panel. Show completion only for fields actually populated, never as approval. Describe ticks as Kevin’s own progress aid.
- **1.5 Request details: pre-fill and required fields [P2]**
  - **Issue:** Assumption as rule. Section 1 appears pre-filled with the requester’s details, and “required” fields are shown without a defined set. Facility ID alone was called required, with no source.
  - **Evidence status:** **A** for the pre-fill source and the required set. **S** for facility ID (Felix, source not cited).
  - **Validation needed:** Field list in the client UAT demo; data dictionary. Cohen for where requester details come from.
  - **Recommended change:** Use one required-field marker taken from the UAT demo. Log any field made required on the team’s own judgment as a hypothesis. Keep pre-filled fields editable.
- **1.6 Help text and building look-up [P2]**
  - **Issue:** Assumption as rule. Guidance pop-ups and any facility or building look-up can read as official Infrastructure wording and as a live link to building data. The 1 Oct decision limits BLIMS to a placeholder.
  - **Evidence status:** **S:** “no one knows what the building code is” (Kai); not a pain for the PM-side interviewee. **A:** what BLIMS holds is unknown to the team.
  - **Validation needed:** Cohen or a technical contact on building data. Infrastructure for guidance wording.
  - **Recommended change:** Inline help only, worded from the existing checklist or marked “content to be supplied”. No auto-complete. Label any look-up “Future: building data, not validated”.
- **1.7 Quantity threshold and lead time [P1]**
  - **Issue:** Assumption as rule. The earlier HTML demo appeared to change lead time above a quantity threshold (“greater than 9”). The 3 October brief attributes lead times to the June 2019 checklist: 12, 8 and 4 weeks by request type. “Greater than 9” counts workstations, not furniture quantity, so fourteen chairs must not trigger it.
  - **Evidence status:** **S.** The June 2019 checklist, as cited in the brief; not independently seen. Whether Greater than 9 and STIP are standalone values or contextual rules is unresolved.
  - **Validation needed:** The checklist itself; furniture coordinator or Cohen.
  - **Recommended change:** Show lead times only as planning guidance from the 2019 checklist, never as a delivery date. Do not apply the Greater than 9 rule to furniture quantity.
- **1.8 Attachments and Infrastructure Attachments [P1]**
  - **Issue:** Assumption as rule. The client UAT build has two upload steps. The second was dropped from Kevin’s journey on an unconfirmed reading of what it is for. If that reading is wrong, a required input has been removed.
  - **Evidence status:** **C** that both steps exist. **A** for what the second holds (one member’s hypothesis). **S:** PM-side requests have no separate infrastructure step.
  - **Validation needed:** Cohen, Wednesday 7 Oct (Q1). No owner was assigned.
  - **Recommended change:** Keep the removal, recorded as conditional. Put the question in the email to Cohen. Show coordinator documents in Scenario 2 as read-only.
- **1.9 Review and validation [P2]**
  - **Issue:** Inconsistent. The demo reached “Request submitted” while required items were flagged as missing. Gaps are also flagged on the attachments step, possibly in different wording.
  - **Evidence status:** **N/A.** Internal consistency, not an evidence question.
  - **Validation needed:** None.
  - **Recommended change:** Two review states: complete, and incomplete with an error summary linking to each field. Keep Submit enabled and explain errors on submit, as GoA guidance advises against disabled buttons. One wording for gaps everywhere. Record the video on the complete path.
- **1.10 Save draft [P2]**
  - **Issue:** Inconsistent. Save draft is on every step in the HTML version, with auto-save and drafts on the home page. How the Figma file handles drafts is not on the record. Test question 2 depends on it.
  - **Evidence status:** **S:** Kai saves a draft, then changes status on a separate tab (F-WORTS has no submit button). Auto-save is **H**.
  - **Validation needed:** Usability test, Q2.
  - **Recommended change:** One Save draft control in the same position on every step, and a Draft status on the list. Show “Draft saved” as a static message; do not claim auto-save in the narration.
- **1.11 Request submitted page [P1]**
  - **Issue:** Missing. The last screen before the “black box” should give the work order number, current stage, who holds the request, what happens next and whether Kevin must act. It has been described both as the end of Scenario 1 and the start of Scenario 2.
  - **Evidence status:** **C** for the problem: furniture-side and PM-side interviewees both lose sight of the request here. **H** for the content. Guiding Scenario: “received and awaiting initial review”.
  - **Validation needed:** Usability test, Q3 and Q4.
  - **Recommended change:** Add the five facts. End Scenario 1 on this page; begin Scenario 2 from it (see 2.1).
- **1.12 Progress indicator [P2]**
  - **Issue:** Inconsistent. The earlier build’s indicator shows six steps: Before you start, Client checklist, Request type, Request details, Supporting documents, Review and submit. The 3 October decision is four steps. The HTML reference bar was reported with five.
  - **Evidence status:** **TD** (3 Oct). Six-step labels seen in the pasted earlier build.
  - **Validation needed:** None.
  - **Recommended change:** Four steps with identical labels on every screen: Request Type, Request Details, Attachments, Review & Submit.

## Scenario 2: after submission

- **2.1 Start of Scenario 2 [P1]**
  - **Issue:** Open decision. Starting at Fulfilling skips the silent interval where the black-box evidence sits. Not decided on Saturday (C6). The pasted earlier build already opens Scenario 2 at “Client approval pending”, so that interval is not shown.
  - **Evidence status:** **C** for the black box, from both sides. Guiding Scenario shows the moment (assigned to Joy, nothing needed from Kevin) but is a team source.
  - **Validation needed:** Usability test, Q3.
  - **Recommended change:** Start at Submitted: stage, holder, last change, “No action needed”. Then the proposal notification. Fulfilling and Closed stay as non-interactive states.
- **2.2 Stage tracker [P1]**
  - **Issue:** Assumption as rule. Submitted, Reviewing, Fulfilling and Closed are shown as the process. “Gatekeeping” appears but no role by that name exists in the scenarios. The Chair flagged exact statuses as unconfirmed.
  - **Evidence status:** **H.** Nobody in Infrastructure has confirmed the names.
  - **Validation needed:** Cohen’s own workflow (received 1 Oct; comparison never assigned). Then an infrastructure-side user. Cohen Q4.
  - **Recommended change:** Keep the four stages as a stated hypothesis. Adekunle compares them with Cohen’s workflow before Wednesday. Remove “gatekeeping” or name the role.
- **2.3 Client decision wording [P1]**
  - **Issue:** Inconsistent. Five wordings were reported: Authorization, Client decision pending, Waiting on client, Client approval pending, Client approved. The pasted earlier screens use “Client approval pending” on the list, header and Approval field; the 3 October brief says “Client decision pending”. It was decided as a status within Reviewing, and the wording is not final (C4).
  - **Evidence status:** **H** for the wording. The need for a client decision is supported (the Chair called it evidenced), but the source interview was not named.
  - **Validation needed:** Infrastructure-side user on stage versus status. Record Anne-Marie’s position.
  - **Recommended change:** Keep “Reviewing” as the stage. Add the sub-status pair “Waiting on client decision” (action with Kevin) and “Client decision recorded”, in identical words on list, tracker, notification and header.
- **2.4 Proposal view [P1]**
  - **Issue:** Missing. The proposal is shown inside the work order, under its number, title and location, in the earlier build. It has one “Estimated cost: Not supplied” and no delivery cost per source, and it names “Snap Tracker” (availability source) and “ROSS furniture” (vendor), which no source supports. Members described its contents differently.
  - **Evidence status:** **TS.** The Guiding Scenario fixes the contents: four recycled and ten new chairs, furniture costs, delivery cost per source, timing. Pictures were doubted.
  - **Validation needed:** Furniture coordinator: what a standard proposal contains.
  - **Recommended change:** Show the proposal under its work order with only the supported contents: quantity from each source, furniture and delivery cost per source, timing, total, marked “Not supplied” where unknown. Remove “Snap Tracker” and “ROSS furniture” unless a source is produced.
- **2.5 Sharing and approval mechanism [P1]**
  - **Issue:** Open decision. “Share externally”, a package button, a signable document and a client Approve button each assert a capability nobody has confirmed. An Approve button would also make the client an actor. The earlier build shows neither a package control nor a decision control, only “This prototype does not let Kevin approve on the client’s behalf.”
  - **Evidence status:** The need is supported (everything for the decision in one place, and a way back). **A** for every mechanism. Sending documents out of an internal system has not been put to Cohen.
  - **Validation needed:** Cohen Q5: how the proposal reaches the client today and what counts as approval.
  - **Recommended change:** Build “Download proposal package” and “Record client decision” (outcome, approver’s name, date, optional attached confirmation). Label any Share control “Concept, not validated”.
- **2.6 Client decision outcomes [P2]**
  - **Issue:** Missing. Every account assumes approval. Nothing shows a request for changes or a decline, or what Joy sees next.
  - **Evidence status:** **None** either way.
  - **Validation needed:** Cohen Q6, or a furniture coordinator.
  - **Recommended change:** Offer Approved, Changes requested and Declined in “Record client decision”. Link only Approved. Name the other two as boundaries in the video.
- **2.7 Return path [P2]**
  - **Issue:** Missing. Kevin must be able to step out to obtain the decision and come back without losing his place. No return route has been drawn.
  - **Evidence status:** **H.** Rests on the team’s reasoning about Kevin’s workload; not put to a CMAC.
  - **Validation needed:** Usability test, Q4.
  - **Recommended change:** The list row reads “Waiting on client decision, action with you” and opens at the proposal panel.
- **2.8 Current holder [P1]**
  - **Issue:** Assumption as rule. A named holder is shown from the moment of submission in some accounts. That presumes someone is assigned at every stage, that PRISM knows who, and that names may be shown to requesters. The earlier build shows “Current owner: Kevin” while the request waits on the client; the new list shows “Joy — Furniture Coordinator” for the same state.
  - **Evidence status:** **C** for the need to know who has the request. **A** that a name is available. **S:** shared mailbox (PM-side only). Guiding Scenario names Joy only after the Furniture Request Coordinator’s review.
  - **Validation needed:** Infrastructure-side user. Cohen Q7.
  - **Recommended change:** Show role first, name second. Add “Awaiting initial review, not yet assigned” for Submitted.
- **2.9 Role names [P2]**
  - **Issue:** Inconsistent. Two Infrastructure roles are involved: the Furniture Request Coordinator (reviews and assigns) and the Furniture Coordinator, Joy (prepares the proposal). Screens and speech use FRC, coordinator and Joy interchangeably.
  - **Evidence status:** **C** that both roles exist (1 Oct). Exact titles unconfirmed.
  - **Validation needed:** Cohen for exact role titles (Q4).
  - **Recommended change:** Titles in full, no acronyms. One persona name per role, matching the Requirements Document.
- **2.10 Activity and messages [P2]**
  - **Issue:** Missing. A two-sided history was agreed but its placement was not. The earlier build has a “Message Joy” composer and two activity events, but no message from Joy in the history. The willingness test Felix proposed has no owner.
  - **Evidence status:** **H.** No evidence that Infrastructure staff will message inside PRISM.
  - **Validation needed:** Infrastructure-side user. Usability test.
  - **Recommended change:** One Activity timeline per work order, mixing status changes and messages, each with role, name and time. Put it on the right, the same side as the Scenario 1 panel.
- **2.11 Notifications [P2]**
  - **Issue:** Inconsistent. The 1 October decision: a notification signals a change and returns the user to PRISM. The earlier build has a separate Notifications page (“Mark all read”); the 3 October brief removes it.
  - **Evidence status:** **S:** CMACs do not open the legacy system’s emails (Demo 2); one PM-side complaint about repeats; the same interviewee showed little interest in status notifications.
  - **Validation needed:** Usability test.
  - **Recommended change:** Use an unread marker on the list and in the menu that opens the request at the relevant tab and clears only the unread state. No separate Notifications page. Show email only as a concept frame.
- **2.12 Later stages, dates and closure [P3]**
  - **Issue:** Assumption as rule. Fulfilling and Closed are shown but not designed. Any target date or service standard would be invented, and nothing should imply that Kevin closes the request.
  - **Evidence status:** **A.** Nothing on the record.
  - **Validation needed:** Cohen Q8: who closes a request; service standards.
  - **Recommended change:** Show real event times only (submitted, last updated). Grey the later stages, marked “Not covered in this prototype”. No Close control for Kevin.

## Across both scenarios

- **3.1 Client outside the system [P2]**
  - **Issue:** Assumption as rule. The 3 Oct decision is a scope choice, but it was argued as policy (“clients are not meant to use an internal system”). On 1 Oct Cohen was reported to describe clients entering requests and the CMAC checking them.
  - **Evidence status:** **TD** (3 Oct). **A** as a rule. **S** against it (Cohen, as recalled by Anne-Marie).
  - **Validation needed:** Cohen Q9, Wednesday.
  - **Recommended change:** Say “out of scope for this prototype”, never “not permitted”. Record other user groups as a design principle in the Requirements Document. Do not build the client-contact section until decided.
- **3.2 Sample data across scenarios [P1]**
  - **Issue:** Inconsistent. One request should travel through both scenarios. The same record appears as “Not supplied”, “Work Order #001” and “PR-2026-1027” in the pasted screens. “Task chairs” appears in the prototype but not in the Guiding Scenario (“fourteen chairs”) or the brief (“fourteen additional chairs”).
  - **Evidence status:** **TS.** The Guiding Scenario fixes the case: fourteen chairs, McDougall Centre, Calgary, recycled preferred.
  - **Validation needed:** None.
  - **Recommended change:** Pin one sample-data sheet in the file (draft in Appendix B). Both builders copy from it.
- **3.3 Status vocabulary [P1]**
  - **Issue:** Inconsistent. Status words differ between list, tracker, notification and discussion. The pasted screens use Draft, Client approval pending, Action needed, Under coordination, Reviewing and Closed. Colour is allowed only with the stage label (1 Oct).
  - **Evidence status:** **TD** (1 Oct on colour). No vocabulary agreed.
  - **Validation needed:** Stage names with Cohen (see 2.2).
  - **Recommended change:** One status table: label, meaning for Kevin, holder, Kevin’s action (draft in Appendix B). Label always beside colour. Copy into the data dictionary.
- **3.4 Product name [P2]**
  - **Issue:** Inconsistent. The prototype header reads “PRISM Request”. Revision 2 and the team’s documents say “PRISM Requests”. WORTS 2 (Cohen’s interim suggestion, as reported) and a file titled “Wort2” were also in use.
  - **Evidence status:** **S.** WORTS 2 is Cohen’s interim suggestion, as reported by Mmenyene.
  - **Validation needed:** Cohen Q10, in writing.
  - **Recommended change:** Choose one name and use it on the file, screens, video and documents. The prototype and brief use “PRISM Request”.
- **3.5 Balance between the scenarios [P1]**
  - **Issue:** Missing. Scenario 1 is nearly complete and Scenario 2 is “very rough”, yet post-submission visibility is the strongest evidence. Without it the prototype reads as a refinement of form submission.
  - **Evidence status:** **C** for post-submission visibility (both sides). Entry pain rests on **S** (Kai); PM-side interviewees were content.
  - **Validation needed:** Cohen’s reaction on Wednesday.
  - **Recommended change:** Hold the link to Cohen until Scenario 2 is as complete as Scenario 1. Tie each Scenario 1 change to Kai’s evidence in the briefing.
- **3.6 Usability plan traceability [P2]**
  - **Issue:** Missing. Each of the four accepted test questions needs a screen that can answer it. The Figma file had no dashboard; whether its list shows drafts or a needs-action marker is not on the record.
  - **Evidence status:** **TD** (1 Oct).
  - **Validation needed:** The test itself; testers sourced through Cohen.
  - **Recommended change:** Add a one-line “Next step” to every work order state. Map each test task to a frame before testers are booked (map in section 6.2).
- **3.7 Boundaries [P3]**
  - **Issue:** Missing. Intake, the coordinator dashboard, BLIMS and fulfilment are excluded by decision, but nothing on the screens or in a script says so. Intake by shared mailbox is unconfirmed; the questions for Kai have no owner.
  - **Evidence status:** **S** for the shared mailbox (PM-side).
  - **Validation needed:** Kai, by email.
  - **Recommended change:** One caption at the start of Scenario 1 (“Kevin has received a client request; intake is outside this prototype”) and a boundaries list for the video. Assign the email to Kai.
- **3.8 Fidelity and build method [P1]**
  - **Issue:** Open decision. The deliverable has been called both low and mid fidelity. The working file is still a Figma Make file, edited by prompting, while the instructor’s reported expectation is a largely manual Figma build.
  - **Evidence status:** **S:** an oral account of the instructor’s position. The brief was not read into the record.
  - **Validation needed:** Teaching team’s reply (A1). Assignment 3 brief.
  - **Recommended change:** Read step one of the brief into today’s record. Add no generated screens until the reply arrives; keep a short log of what was built by hand.
- **3.9 WORTS screens in the video [P2]**
  - **Issue:** Assumption as rule. The video is to compare the prototype with the client’s existing WORTS screens, on YouTube. The Charter treats client material as Protected A.
  - **Evidence status:** **A** that the screens may be published. Nobody has asked.
  - **Validation needed:** Cohen Q11, written permission or a ruling.
  - **Recommended change:** Ask. If refused or unanswered, redraw the old flow as a schematic and set the video to unlisted.

## Decisions needed today

- **Checklist step:** remove it; side panel during entry, full checklist on a Help page, one tick on review only if Cohen requires it (1.3, 1.4).
- **Client decision wording:** “Reviewing” stays the stage; add “Waiting on client decision” and “Client decision recorded” (2.3).
- **Sharing and approval:** “Download proposal package” and “Record client decision”; any share control labelled a concept (2.5, 2.6).
- **Start of Scenario 2:** start at Submitted, nothing needed from Kevin, then the proposal notification (2.1).
- **Link for Cohen:** one link, sent once Scenario 2 is as complete as Scenario 1 (3.5, 3.8).
- **Other user groups:** design principle and future-state note, no build (3.1).
- **Product name:** one name everywhere, confirmed with Cohen (3.4).
- **Unowned work:** status table, sample-data sheet and workflow comparison to Adekunle by Tuesday; Help page to Felix; Kai email and video script to be assigned (2.2, 3.2, 3.3, 3.7).

## Questions for Cohen, Wednesday 7 October

1. What goes into Attachments and Infrastructure Attachments in the UAT build, and who uploads each? (1.8)
2. Is the client checklist a record to attest or attach, or guidance? (1.3)
3. Which fields are mandatory, and where do the requester’s details come from? (1.5)
4. Do Submitted, Reviewing, Fulfilling and Closed match Infrastructure’s lifecycle, and under what role titles? (2.2, 2.9)
5. How does a proposal reach the client today, and what counts as approval? (2.5)
6. What happens when the client asks for changes or declines? (2.6)
7. May the requester see the name of the person holding the request? (2.8)
8. Who closes a request, and are there service standards? (2.12)
9. Is direct entry of requests by clients intended? (3.1)
10. Which product name should the screens carry? (3.4)
11. May WORTS screens appear in an unlisted YouTube video? (3.9)
