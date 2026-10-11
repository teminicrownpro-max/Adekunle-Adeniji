# Canadian Graduate Strategy for Adedamola Adetola

**Basis:** CV (B.Eng. Mechanical, First Class, ABUAD/ATU Ibadan, Mar 2025; UAV Technician at Aerotech; machining, CAD, EASA A1/A3, FAA UAS certificates).
**Not available:** the portfolio (adedam100.github.io) did not resolve from my environment, so nothing below uses it. Add anything it contains (projects, GPA, publications).
**Verification legend:** ✅ = confirmed in a source I opened or searched this session. ⚠️ = not confirmed; check before relying on it.
**Not verified for any professor:** whether they are accepting students in the 2027 cycle. Check each lab page and the program's admissions page before emailing.

---

## 1. Positioning (the strategic read)

**Strengths:** a hands-on UAV and machining profile, which is rare among applicants. You do real diagnostics on multirotors and FPV drones (ESC and structural faults), you design in Inventor and Fusion, and you fabricate on lathe and mill. A first-class degree gives you the grades.

**Weaknesses to fix before applying:**
- No publications, and no research assistantship on the CV. The Aerotech work is technician-level, so frame it as *fault logs and field data*.
- No GPA or percentage is stated. Add it with the conversion.
- No final-year project with measured results. Quantify the Grain Grinding Machine and the Drone Design projects (throughput, mass, thrust, test results).
- Transport Canada RPAS credentials are absent. Canadian labs value them for flight testing, so consider the Advanced Operations certificate.

**Recommended path:** MASc (thesis) first, then a PhD later if it fits. Do not apply directly to a PhD: with no publications, funded PhD offers are unlikely. A course-based MEng is the safety net, not the plan. MEng programs are generally not funded and are usually not a route into a PhD (aggregators note Concordia directs doctoral aspirants to its MASc ⚠️).

---

## 2. Ranked targets

| Tier | School / supervisor | Fit with your profile | Why |
|---|---|---|---|
| **Best fit** | **Concordia, Dr. Youmin Zhang** (Mech., Industrial & Aerospace Eng.; CIADI) ✅ | Your ESC and structural fault diagnosis maps onto his core area | His research covers guidance, navigation and control, fault diagnosis and fault-tolerant control for UAVs, and his labs (DFCSL, NAVL) use quadrotor testbeds ✅. He has a 2023 Springer book on fault-tolerant cooperative UAV control ✅. |
| **Best fit** | **University of Victoria, Dr. Afzal Suleman** (Canada Research Chair, Aerospace Systems) ✅ | Design, fabrication and flight testing | He directs a centre combining multidisciplinary design optimization with subscale UAV flight testing, with industry partners (Boeing, Embraer, Bombardier) ✅. Your machining and CAD skills are an asset here. |
| **Reach** | **University of Toronto, Dr. Hugh H.T. Liu** (UTIAS, Flight Systems & Control; CARRE director) ✅ | Strong lab, high competition | The lab works on multi-quadrotor payloads, eVTOL and GNSS-denied flight ✅. Admission is very competitive, and the UAV emphasis requires specific courses ✅. |
| **Target** | **University of Calgary, Dr. Mahdis Bisheban** (Intelligent Dynamics & Control Lab) ✅ | Control and learning on drones | Topics include manipulator-equipped drones, wind-field simulation and RL controllers ✅. More control-theory heavy than your CV. |
| **Optional** | **Toronto Metropolitan University, Dr. Guangjun Liu** (SOTI Research Chair, Aerospace) ✅ | Control and robotics | Chair created to lead drone and UAV research (2022) ✅. Check current openings. |
| **Not recommended as first target** | **Polytechnique Montréal, Dr. Giovanni Beltrame** (MIST Lab) ✅ | Swarm and autonomy | The home department is Computer & Software Engineering ✅, which favours software-heavy applicants. |

**Course-based fallbacks** (confirm each on the official page):
- Concordia M.Eng. Aerospace is the only one of the schools I checked that is confirmed course-based ✅ (aggregator listing; fees are inconsistent across sources, so use Concordia's own page).
- McGill M.Eng. Aerospace is course-based ✅.
- TMU M.Eng. Aerospace and U of T (UTIAS) M.Eng. exist as professional programs, but their course-based status was not confirmed ⚠️.

**Application order:** Zhang and Suleman as primary targets, Calgary and Toronto as reaches, Concordia M.Eng. as the fallback. Contact 8 to 10 people in total, in staggered batches.

---

## 3. Research proposals (each sized for a 2-year MASc)

### A. For Dr. Zhang: *Early detection and tolerance of ESC and motor-driver faults in multirotors using flight-log and current-telemetry data*

**Gap.** Fault diagnosis for multirotors concentrates on propellers and motors. In the work I found, ESC faults are mentioned as one part of the powertrain rather than studied directly. Examples: Bondyra et al. (2018, vibration-based blade damage); Cacace et al. (2024, J. Intelligent & Robotic Systems, motor-fault detection via an external-wrench estimate and an RNN); and a 2019 Berkeley study on vibration-based propeller diagnosis ✅. Nearly all of it is simulation or lab-bench work. ⚠️ I did not find an ESC-specific review in one search, so run a systematic search before claiming novelty.

**Research questions.**
1. Which ESC fault signatures (desync, thermal derating, FET failure, signal loss) are observable from standard flight-controller logs?
2. Can a lightweight detector run on-board and still separate ESC faults from motor and propeller faults?
3. Does fault-tolerant reallocation improve landing outcomes under ESC dropout?

**Method.** Build a quadrotor and hexarotor rig (your skills), inject ESC faults in a bench and tethered setup, collect labelled telemetry, then compare model-based residuals against a small learned classifier. Validate with controlled flights, and deploy on Quanser-class hardware if the lab offers it.

**Contribution.** A labelled ESC-fault dataset and a benchmark, a deployable detector, and a tolerance strategy.

**Feasibility.** It uses your direct experience diagnosing ESC faults at Aerotech.

### B. For Dr. Suleman: *Design-for-manufacture MDO of a small multirotor/VTOL airframe with machined and printed structure*

**Gap.** MDO reviews cover aerial vehicles broadly (e.g. Papageorgiou et al., 2018, *Int. J. Aerospace Engineering*, DOI 10.1155/2018/4258020 ✅), but manufacturing cost and process limits, such as machining or printing constraints, are rarely built into the optimization loop for small UAVs. ⚠️ I did not read the full text; check its "gaps" section.

**Research questions.**
1. How much mass or cost does including manufacturing constraints change in the optimum?
2. Does a surrogate-assisted loop keep the cost of that extra fidelity affordable?

**Method.** Parametric CAD (Inventor/Fusion), FEA, surrogate-based optimization, then fabricate and flight-test two variants (conventional versus manufacturing-aware).

**Contribution.** A reproducible workflow and measured validation on real hardware.

### C. For Dr. H. Liu (UTIAS): *Fault-aware control for multi-quadrotor slung payload transport*

**Gap.** The lab's published work covers robust cooperative control of quadrotors carrying payloads: Qian and Liu, *J. Guidance, Control, and Dynamics* (2022), DOI 10.2514/1.G006173 ✅, and Chen, Shan and Liu, *Int. J. Aerospace Engineering* (2022), DOI 10.1155/2022/2486561 ✅. ⚠️ I did not confirm whether motor or ESC degradation inside a cooperative payload setting is covered. Verify with a literature search first.

**Research questions.**
1. How does partial loss of thrust on one carrier alter payload stability?
2. Can the team reallocate load safely?

**Method.** Extend the existing dynamics model with actuator-degradation terms, then design a robust reallocation controller, with simulation first and a small indoor test if the lab agrees.

**Why this one:** it fuses your diagnostics experience with the lab's own research line. It is the highest-reach option.

*(A fourth, for Dr. Bisheban, can follow the same pattern: learning-based fault-tolerant control of a drone with a manipulator. I would not draft it until you confirm interest.)*

**Foundational literature (verified):**
- Zhang, Y. & Jiang, J. (2008). Bibliographical review on reconfigurable fault-tolerant control systems. *Annual Reviews in Control*, 32(2), 229–252. DOI 10.1016/j.arcontrol.2008.03.008 ✅
- Yu, Z., Zhang, Y., Jiang, B., Su, C.-Y. (2023). *Fault-Tolerant Cooperative Control of Unmanned Aerial Vehicles*. Springer. ISBN 978-981-99-7660-7 ✅ (author order as listed by a retailer; confirm)
- Qian, L. & Liu, H.H.T. (2022). Robust path-following control for multiple quadrotors with a slung payload. *JGCD*. DOI 10.2514/1.G006173 ✅ (title wording approximate; the page confirmed authors, journal and DOI)
- Papageorgiou, A., Tarkian, M., Amadori, K., Ölvander, J. (2018). Multidisciplinary design optimization of aerial vehicles: a review of recent advancements. *Int. J. Aerospace Eng.* DOI 10.1155/2018/4258020 ✅
- Cacace et al. (2024). Motor fault detection and isolation for UAVs with an external-wrench estimate and RNN. *J. Intelligent & Robotic Systems* ✅ (volume and pages not captured)

I could not reach Crossref from this environment, so cross-check DOIs and bibliographic details in Google Scholar before citing.

---

## 4. Cold emails

Rules: send from your own address, one email per professor, attach the CV (and a 1-page proposal summary), and personalise the bracketed hooks by reading one recent paper from the lab. Keep each under 200 words.

### Dr. Youmin Zhang (Concordia)
**Subject:** MASc inquiry: fault diagnosis for multirotor ESC and motor faults

Dear Professor Zhang,

I am a First Class B.Eng. Mechanical Engineering graduate (ABUAD/ATU Ibadan, 2025) and currently a UAV technician in Lagos, where I diagnose ESC and structural faults on multirotor and FPV drones. I hold EASA A1/A3 and FAA UAS certificates.

Your work on fault diagnosis and fault-tolerant control for UAVs, especially [paper or Quanser testbed work], matches what I see in the field. I have noticed that ESC faults are often treated as part of the powertrain rather than as their own diagnostic problem, and I would like to study early detection of ESC and motor-driver faults from flight-controller telemetry, with a tolerance strategy for the failure case. I have drafted a one-page outline and can build the test rig myself.

Are you considering MASc students for [Fall 2027]? If so, I would welcome your advice on fit and on funding routes. My CV and outline are attached.

Thank you for your time.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com | [LinkedIn]

### Dr. Afzal Suleman (UVic)
**Subject:** MASc inquiry: manufacturing-aware design optimization for small UAV airframes

Dear Professor Suleman,

I am a First Class Mechanical Engineering graduate with hands-on experience in design (Inventor, Fusion 360), machining (lathe, mill) and UAV maintenance, and I hold EASA A1/A3 and FAA UAS certificates. I am drawn to your centre's combination of multidisciplinary design optimization and subscale flight testing.

I am interested in a question that I think is under-studied for small UAVs: how much the optimum changes when manufacturing constraints such as machining and printing limits are built into the optimization loop, validated by building and flying both variants. My drone design and fabrication projects have prepared me to do the build side myself.

Are you taking MASc students for [Fall 2027]? I would be grateful for your view on whether this direction suits your group. CV and one-page outline attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

### Dr. Hugh H.T. Liu (UTIAS)
**Subject:** MASc inquiry: fault-aware cooperative payload transport with quadrotors

Dear Professor Liu,

I am a First Class B.Eng. Mechanical graduate and a UAV technician who diagnoses ESC and structural faults on multirotors. I have read your group's work on multi-quadrotor payload control, notably Qian and Liu (JGCD, 2022), and I would like to explore what happens to cooperative payload stability when one carrier suffers partial thrust loss, and how load could be safely reallocated.

I understand the UAV emphasis requires specific courses and am prepared to complete them. Are you considering MASc students for [Fall 2027]? My CV and a short outline are attached. I would value any guidance on how to strengthen my application.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

### Dr. Mahdis Bisheban (Calgary), short form
**Subject:** MSc inquiry: learning-based control for drones with manipulators

Dear Professor Bisheban,

I am a First Class Mechanical Engineering graduate working as a UAV technician (ESC/structural diagnostics; EASA A1/A3, FAA UAS). Your lab's work on drones with manipulators and learning-based controllers fits the practical failure modes I deal with daily. I would like to propose a project on [fault-tolerant control for a drone with an attached arm]. Are you accepting MSc students for [Fall 2027]? CV attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

---

## 5. Next steps (in order)
1. Send me the portfolio contents and GPA, and I will tighten the proposals and emails.
2. Run a proper literature search for each gap (Scopus, Web of Science, Google Scholar) and keep the search strings; this is what will make the "gap" claims defensible.
3. Check each lab and admissions page for 2027 intake, funding, and English requirements.
4. Email the primary targets first, then the reaches, with a staggered one-week follow-up.
