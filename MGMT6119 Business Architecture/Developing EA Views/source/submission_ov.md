---
title: "Developing EA Views – DoDAF OV-1 and OV-2"
subtitle: "MGMT6119 Business Architecture (Online) – Developing EA Views Individual Assignment"
author: "Adekunle Adeniji · Student number 1378471"
date: "November 16, 2026"
---

## 1. Introduction and architecture context

This submission develops two standard DoDAF 2.02 models from the Operational Viewpoint: the **OV-1 High-Level Operational Concept Graphic** and the **OV-2 Operational Resource Flow Description**. Both describe one notional architecture: how a maritime search-and-rescue (SAR) region turns a distress alert into a coordinated rescue, ending with survivors handed to medical care ashore.

The pair was chosen deliberately. OV-1 answers *what is the mission and who takes part* for executives and non-specialists. OV-2 answers *which performers must exchange which resources* in a form that can be analysed and checked. OV-1 frames the concept; OV-2 makes it rigorous. Every OV-2 needline traces back to a numbered OV-1 interaction (Section 4).

The architecture's context is summarised below, in the style of an AV-1 Overview and Summary.

| Item | Description |
| --- | --- |
| Architecture name | Maritime SAR Coordination – "As-Is" operational architecture (notional) |
| Purpose | Show how distress alerts become coordinated rescue action, to expose coordination dependencies and information-exchange needs |
| Viewpoint | Operational Viewpoint: what is done and who does it, independent of any system or technology |
| Scope | From first distress alert to hand-over of survivors to medical care, within one maritime SAR region |
| Performers in scope | Joint Rescue Coordination Centre (JRCC), maritime communications centre, SAR air unit, SAR surface unit acting as On-Scene Coordinator |
| External performers | Vessel and persons in distress, satellite distress-alerting service, vessels of opportunity, meteorological and ocean service, emergency medical services and hospital |
| Out of scope | Systems and networks (Systems Viewpoint), cost, training, public affairs, post-incident investigation |
| Stakeholders | SAR mission coordinators, air and coast guard SAR commanders, emergency planners, enterprise architects |
| Assumptions | Notional and unclassified; based on publicly described SAR practice in the IAMSAR Manual; not an official model of any agency |
| Tool | Both views were drawn as vector diagrams (SVG) following DoDAF 2.02 notation and exported as PNG images |

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 2. View #1 – OV-1 High-Level Operational Concept Graphic

The OV-1 shows the whole mission in one picture: a fishing vessel in distress, the shore-based centres that receive and act on its alert, and the air and sea units that rescue its crew, joined by nine numbered interactions.

![](<../Backup - OV-1 and OV-2 version/OV-1_High-Level_Operational_Concept_Graphic.png>){width=6.5in}

*Figure 1. OV-1 High-Level Operational Concept Graphic – Maritime SAR Coordination (notional).*

**DoDAF definition.** DoDAF 2.02 defines the OV-1 as a high-level graphical and textual description of the operational concept. It shows the mission, the main performers and their environment, and how the architecture interacts with external performers. Its graphic is free-form, but it must be paired with a textual description, which the figure's key and the narrative table below provide.

### 2.1 Key elements of the OV-1

| DoDAF OV-1 element | How it appears in Figure 1 |
| --- | --- |
| Mission or scenario | Banner: detect, locate and rescue persons in distress at sea, and deliver survivors to medical care |
| Operational performers (in scope) | JRCC, highlighted as the coordination hub; maritime communications centre (MCTS); SAR air unit (fixed-wing aircraft and helicopter); Coast Guard cutter acting as On-Scene Coordinator (OSC) |
| External performers | Vessel and crew in distress; satellite distress-alerting service (satellites, ground station, Mission Control Centre); vessels of opportunity; met and ocean service; EMS and hospital |
| Operational environment and locations | Space, air, sea and shore zones, plus the search area drawn around the distress position |
| Interactions (resource flows) | Nine numbered arrows, styled by type: distress signals, information exchanges, and movement of personnel or materiel |
| Textual description | The key inside the figure and the narrative table in 2.2 |

### 2.2 Operational narrative: relationships among the elements

| # | Interaction | From → To | Resource exchanged |
| --- | --- | --- | --- |
| 1 | Distress alert raised | Vessel in distress → satellite system and MCTS | 406 MHz beacon alert; VHF Mayday call |
| 2 | Alert detected, located and distributed | Satellites → ground station and MCC → JRCC | Distress alert message: beacon ID, position, time |
| 3 | Mayday acknowledged and relayed | MCTS → vessel; MCTS → JRCC | Acknowledgement and safety advice; distress relay |
| 4 | Search planned | Met and ocean service → JRCC | Wind, sea-state, current and drift data, used to compute the search area |
| 5 | SAR units tasked | JRCC → SAR air unit and Coast Guard cutter | Tasking orders and search action plan; cutter designated OSC |
| 6 | Vessels of opportunity alerted | JRCC → MCTS → vessels of opportunity | Mayday Relay broadcast; replies with position and ETA |
| 7 | On-scene coordination | OSC ↔ air unit and vessels of opportunity; OSC → JRCC | Search assignments, sightings, situation reports (SITREPs) |
| 8 | Rescue | Air unit and cutter ↔ survivors | Survival equipment dropped (materiel); survivors hoisted or recovered (personnel) |
| 9 | Hand-over | Cutter and helicopter → EMS and hospital | Survivors and casualty reports; the JRCC then concludes the case |

Two relationships matter most. Six of the nine interactions start or end at the JRCC, so it is the hub of the concept. And the alert reaches the JRCC by two independent paths, satellite (1–2) and radio (1, 3), which is redundancy by design.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## 3. View #2 – OV-2 Operational Resource Flow Description

![](<../Backup - OV-1 and OV-2 version/OV-2_Operational_Resource_Flow_Description.png>){height=8.25in}

*Figure 2. OV-2 Operational Resource Flow Description – Maritime SAR Coordination (notional).*

The OV-2 turns the concept into a checkable model: nine operational performers joined by 14 needlines that carry 26 resource flows. Two performers sit on five needlines each: the JRCC, which coordinates, and the On-Scene Coordinator, which executes.

**DoDAF definition.** In DoDAF 2.02 the OV-2 shows the needlines between operational performers. A needline records a need to exchange resources and bundles one or more resource flows. It shows that an exchange is needed, not how it is carried; channels and systems belong to the Systems Viewpoint. Performers may be inside or outside the architecture, and resources may be information, materiel or personnel.

### 3.1 Operational performers

| ID | Operational performer | Scope | Location | Key operational activities |
| --- | --- | --- | --- | --- |
| OP-1 | Vessel and persons in distress | External | At sea | Raise distress alert; signal position; take to life raft |
| OP-2 | Satellite distress-alerting service (Mission Control Centre) | External | Space and ground segment | Detect and locate 406 MHz beacons; distribute alerts |
| OP-3 | Joint Rescue Coordination Centre (SAR Mission Coordinator) | In scope | Ashore | Classify the emergency phase; plan the search; task and coordinate units; conclude the case |
| OP-4 | Maritime communications centre (MCTS) | In scope | Ashore, coastal | Keep distress watch; acknowledge and relay; broadcast Mayday Relay |
| OP-5 | SAR air unit (fixed-wing and helicopter) | In scope | Airborne | Search the assigned area; drop survival equipment; hoist and medevac survivors |
| OP-6 | SAR surface unit, acting as On-Scene Coordinator | In scope | At sea | Coordinate units on scene; recover survivors; land them ashore |
| OP-7 | Vessels of opportunity | External | At sea | Divert, search and assist under OSC direction |
| OP-8 | Met and ocean service | External | Ashore | Provide wind, sea-state and drift forecasts |
| OP-9 | EMS and receiving hospital | External | Ashore | Receive, triage and treat survivors |

### 3.2 Needlines and resource flows

Type: I = information, M = materiel, P = personnel.

| Needline | From → To | Resource flows (type) |
| --- | --- | --- |
| NL1 | OP-1 → OP-2 | RF1 406 MHz beacon alert: beacon ID and encoded position (I) |
| NL2 | OP-2 → OP-3 | RF2 Distress alert message: beacon ID, position fix, time, registration data (I) |
| NL3 | OP-1 ↔ OP-4 | RF3 Mayday call: identity, position, nature of distress, persons on board (I); RF4 Acknowledgement and safety advice (I) |
| NL4 | OP-4 ↔ OP-3 | RF5 Distress relay (I); RF6 Request to broadcast a Mayday Relay (I) |
| NL5 | OP-4 ↔ OP-7 | RF7 Mayday Relay broadcast (I); RF8 Vessel replies: position, ETA, capability (I) |
| NL6 | OP-8 → OP-3 | RF9 Wind, sea-state, current and drift data (I) |
| NL7 | OP-3 ↔ OP-5 | RF10 Tasking and search action plan (I); RF11 SITREPs and sighting reports (I) |
| NL8 | OP-3 ↔ OP-6 | RF12 Tasking, OSC designation and search action plan (I); RF13 OSC SITREPs: area covered, survivors recovered (I) |
| NL9 | OP-6 ↔ OP-5 | RF14 On-scene search assignments (I); RF15 Sightings and datum-marker positions (I) |
| NL10 | OP-6 ↔ OP-7 | RF16 On-scene direction (I); RF17 Search results (I) |
| NL11 | OP-5 ↔ OP-1 | RF18 Air-dropped survival equipment (M); RF19 Distress signals such as flares and homing signal (I); RF20 Survivors hoisted (P) |
| NL12 | OP-6 ↔ OP-1 | RF21 Rescue instructions (I); RF22 Survivors recovered aboard (P) |
| NL13 | OP-6 → OP-9 | RF23 Survivors landed ashore (P); RF24 Casualty hand-over report (I) |
| NL14 | OP-5 → OP-9 | RF25 Survivors on medevac (P); RF26 Casualty report and ETA (I) |

### 3.3 Modelling rules applied to the relationships

- Every needline joins exactly two performers. Arrowheads show the direction of each resource flow, so a two-way needline carries flows both ways.
- A needline states a need, not a channel. Radio, satellite links and networks belong in SV-1 and SV-2, so none appear here.
- The dashed boundary separates the four performers in scope from the five external ones. Each needline crossing it is an external interface the architecture must honour.
- Resource flows cover information (21), materiel (1) and personnel (4), so the physical rescue is modelled as well as the coordination.
- Performer names match the OV-1, which keeps the two views consistent.

## 4. Consistency and traceability between OV-1 and OV-2

The two views agree with no orphans: each of the 14 needlines traces to at least one OV-1 interaction, and each OV-1 interaction is refined by at least one needline.

| OV-1 interaction | OV-2 needlines that refine it |
| --- | --- |
| 1 Distress alert raised | NL1, NL3 |
| 2 Alert detected and distributed | NL2 |
| 3 Mayday acknowledged and relayed | NL3, NL4 |
| 4 Search planned | NL6 |
| 5 SAR units tasked | NL7, NL8 |
| 6 Vessels of opportunity alerted | NL4, NL5 |
| 7 On-scene coordination | NL7, NL8, NL9, NL10 |
| 8 Rescue | NL11, NL12 |
| 9 Hand-over | NL13, NL14 |

The performers map one-to-one, with one deliberate abstraction. The OV-1 draws the satellites, ground station and Mission Control Centre as separate pictures, but the OV-2 rolls them into one performer, OP-2. The OV-2 models who acts on the alert, not the equipment that carries it.

## 5. Critical analysis

Read together, the views reveal two coordination hubs, heavy dependence on parties outside the architecture, and one gap in the information flow. They also have clear limits that further views must cover.

**What the views reveal**

- **Two hubs, two single points of failure.** The JRCC and the On-Scene Coordinator each sit on 5 of the 14 needlines. If the JRCC loses power, staff or communications, tasking stops. A To-Be architecture should add a needline to an alternate or neighbouring rescue centre.
- **Heavy external dependence.** Five of the nine performers are external, and 9 of the 14 needlines cross the boundary. Mission success depends on parties the SAR region does not control, so agreements and shared distress procedures matter as much as internal design. NL1 joins two external performers; it is kept for context because the satellite alert path begins outside the boundary.
- **Redundant alerting is a strength.** The alert can arrive by satellite (NL1, NL2) or by radio (NL3, NL4). Both paths still converge on the JRCC, which reinforces the first point.
- **Information dominates.** 21 of the 26 resource flows are information. Rescue performance therefore depends on how fast and accurate information is, which suggests measures such as time from first alert to first tasking.
- **A gap exposed by modelling.** No needline runs from the JRCC to the hospital. The hospital learns of casualties only from the unit carrying them (NL13, NL14), which leaves little preparation time. A To-Be could add a JRCC medical pre-alert.

**Limitations of the two views**

- The OV-1 is informal. It communicates well but cannot be analysed, and it simplifies, for example by drawing one helicopter for the whole air unit.
- The OV-2 shows no timing, sequence or rules. It cannot show that the JRCC escalates an incident through the IAMSAR uncertainty, alert and distress phases.
- The model is notional. It would need validation by SAR subject-matter experts before any real decision.

**Views that would extend the architecture**

| DoDAF view | What it would add |
| --- | --- |
| OV-5b Operational Activity Model | The activities behind each performer and the flows between those activities |
| OV-3 Operational Resource Flow Matrix | Attributes of each of the 26 flows, such as timeliness, frequency and security |
| OV-6c Event-Trace Description | The time-ordered sequence from alert to hand-over, including the time to first tasking |
| SV-1 Systems Interface Description | The systems that realise each needline, such as beacons, satellite links, radio and data links |

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## References

Department of Defense Chief Information Officer. (2010). *The DoDAF architecture framework version 2.02*. U.S. Department of Defense. https://dodcio.defense.gov/Library/DoD-Architecture-Framework/

International Cospas-Sarsat Programme. (n.d.). *The Cospas-Sarsat system*. https://www.cospas-sarsat.int/

International Maritime Organization, & International Civil Aviation Organization. (2022). *IAMSAR manual: International aeronautical and maritime search and rescue manual* (Vols. I–III). International Maritime Organization.
