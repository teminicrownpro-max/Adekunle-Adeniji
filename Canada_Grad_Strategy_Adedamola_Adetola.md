---
title: "Canadian Graduate Study Strategy"
subtitle: "Adedamola Adetola: supervisors, schools, research proposals, literature and cold emails"
---

**Prepared:** October 2026, for the Fall 2027 intake.

**Sources used:** your CV (PDF) and the About page of your portfolio repository (`Adedam100/Adedam100.github.io`). `adedam100.github.io` itself did not resolve from my environment, so I read the source files on GitHub instead.

**Verification legend:** ✅ confirmed in a source I opened or searched in this session. ⚠️ not confirmed, so check before relying on it.

**Two limits you should know about:**

- I could not confirm that any professor below is accepting students for 2027. Check each lab page, and write to them.
- Crossref was blocked in my environment, so DOIs and bibliographic details were verified through web search only. Cross-check each in Google Scholar before citing it.

# 1. What your portfolio says, and a problem to fix first

Your About page ✅ states these research interests: **UAV design and performance; aerospace structures and lightweight composites; generative design and topology optimization; prototyping; and smart manufacturing.** It also states that you welcome collaboration in manufacturing, machining and aerial-robotics research. These interests drive the supervisor choices below. They also differ from the pure fault-diagnosis angle I took from the CV alone, so the plan now has two tracks: **design-and-structures (primary)** and **UAV diagnostics (secondary)**.

**Fix this before you email anyone.** A professor who clicks your link will see these, and I read them in the repository ✅:

- The **CV page** still shows the template's sample content: "Ph.D. in Version Control Theory, GitHub University (expected 2018)", "M.S. in Jekyll", "Research Assistant … Professor Hub", and "signed in to 43 Slack teams".
- The **Publications** folder holds five template placeholders with titles like "paper-title-number-1" dated 2009 to 2025.
- The **Portfolio** items are still "Portfolio item number 1".
- The About page says you are **MNSE** (member), while your CV says **Graduate Member** of the Nigerian Society of Engineers. Make them match.

An applicant whose website shows a fake PhD will be dismissed. Either replace these pages with your real CV and two or three real projects, or take them down and share only your PDF CV.

# 2. Positioning

**Strengths.** First Class Honours; hands-on UAV assembly, diagnostics and flight support; machining (lathe, mill); CAD (Inventor, Fusion 360, AutoCAD); a generative-design event certificate ✅ (listed on your portfolio); and EASA A1/A3, FAA UAS and Eurocontrol credentials. Few applicants can both design and build, and that fits experimental labs.

**Weaknesses.** No publications or research assistantship; no stated GPA; no measured results for your projects; no simulation or FEA skills listed yet (essential for topology optimization). Close this last gap before you apply, for example with Fusion 360 generative design or a free FEA tool and one worked UAV-arm example that you document.

**Recommended path.** Thesis-based **MASc first**, then a PhD if a project and funding line up. A direct PhD is unlikely without publications. A course-based master's (MEng) is the safety net: it is usually self-funded, and it is generally not a route into a PhD.

**Timing.** Many Canadian engineering programs close between December and February for Fall entry ⚠️. Confirm deadlines now and email professors in the next two to three weeks.

# 3. Ranked supervisors and why

| Priority | Supervisor and school | Match to your interests | Evidence ✅ |
|---|---|---|---|
| **1** | **Dr. Mehdi Hojjati**, Concordia (Mechanical, Industrial & Aerospace Eng.; CIADI) | Lightweight composites, composite manufacturing, 3D printing, prototyping | Lists composite manufacturing, automated fibre placement, 3D printing, sandwich structures, composite design and analysis; about ten years at NRC Canada before joining Concordia in 2012; the Concordia Centre for Composites has AFP, manufacturing and testing labs |
| **2** | **Dr. Damiano Pasini**, McGill (Mechanical Eng.) | Topology optimization, lightweight lattices, manufacturing defects | Architected Metamaterials Group; interests include topology, shape and size optimization, and robust optimization with manufacturing uncertainties and defects |
| **3** | **Dr. Afzal Suleman**, University of Victoria (Canada Research Chair, Aerospace Systems) | UAV design and performance, MDO, flight test | Directs a centre combining multidisciplinary design optimization with subscale UAV flight testing; industry partners include Boeing, Embraer and Bombardier |
| **4** | **Dr. Abbas Milani**, UBC Okanagan (Mechanical Eng.; MMRI) | Smart and sustainable manufacturing, composite design optimization | Tier 1 Principal's Research Chair in Sustainable & Smart Manufacturing; multi-criteria design optimization of composite and biocomposite structures; the Composites Research Network was recruiting graduate students (undated page) |
| **5** | **Dr. Youmin Zhang**, Concordia (same institute as Hojjati) | UAV diagnostics and fault-tolerant control (your day job) | Fault diagnosis and fault-tolerant control for UAVs; labs DFCSL and NAVL with quadrotor testbeds; 2023 Springer book on fault-tolerant cooperative UAV control |
| **Reach** | **Dr. Pascal Hubert**, McGill (Werner Graupe Chair, Sustainable Composites Manufacturing) | Composites processing and aerospace | Out-of-autoclave and thermoplastic composites; partners include Boeing and Toray. No link to 3D printing found, so frame it as composites manufacturing |
| **Reach** | **Dr. Hugh H.T. Liu**, University of Toronto (UTIAS, CARRE) | UAV systems and control | Multi-quadrotor payload control, eVTOL; very competitive; the UAV emphasis requires specific courses |

**Why Concordia is the strategic anchor.** Hojjati and Zhang sit in the same institute, CIADI. One application to the MASc in Mechanical or Aerospace Engineering gives you two strong supervisor fits, and Concordia also offers a course-based **M.Eng. in Aerospace** ✅ as a fallback.

**Why not more diagnostics-heavy or software-heavy schools.** I dropped the Calgary, Toronto Metropolitan and Polytechnique Montréal targets from my first list. They emphasise control and swarm software, which matches your CV less well than your stated interests in structures and manufacturing.

**Course-based master's options** (confirm each on the official page):

- **Concordia M.Eng. in Aerospace Engineering** is course-based ✅ (aggregator listing; fees differ between sources, so use Concordia's own page).
- **McGill M.Eng. in Aerospace Engineering** is non-thesis ✅.
- Toronto Metropolitan and U of T (UTIAS) both offer professional M.Eng. programs, but I did not confirm that they are course-based ⚠️.

**Realistic PhD route.** Pasini, Milani and Hojjati run PhD programs, but a PhD needs a funded project and usually a master's with a publication. Plan the MASc so that it yields one conference paper and one journal manuscript.

# 4. Research proposals

Each is scoped for a two-year MASc and built on skills you already have.

## Proposal A, for Dr. Hojjati: Load-case-driven concurrent topology and fibre-path optimization of continuous-fibre 3D-printed UAV airframe parts

**Gap.** A 2026 review of generative-design drone frames made by fused deposition modelling ✅ (EPJ Web of Conferences, DOI 10.1051/epjconf/202636701003) reports that adding additive-manufacturing constraints cut weight by 20 to 60% while holding stiffness-to-mass, and lists **anisotropic material behaviour and fatigue as open problems**. It calls for hybrid composites, multi-objective optimization and real-world testing. Separately, reviews of topology optimization for continuous-fibre additive manufacturing ✅ (Gandhi and Minak, *Applied Sciences*, 2022) show that concurrent topology and fibre-orientation methods exist, and recent work (Mokhtarzadeh, López Jiménez and Maute, *Structural and Multidisciplinary Optimization*, 2024 ✅) develops them. ⚠️ My reading of the abstracts is that this concurrent work is demonstrated on generic benchmarks and not validated against UAV flight loads and fatigue; verify this with a systematic search before claiming novelty.

**Research questions.**

1. How much mass can concurrent topology and fibre-path optimization remove from a multirotor arm or motor mount compared with a topology-only design printed in unfilled polymer?
2. Do the optimized parts survive the real load spectrum (thrust, vibration, hard landing) in bench fatigue and drop tests?
3. How sensitive are the gains to printing defects such as voids and fibre misalignment?

**Method.** Extract load cases from instrumented flights (thrust and vibration). Run concurrent optimization. Print baseline and optimized parts on Concordia's composites equipment, then run bench static, fatigue and drop tests. Compare predicted and measured results.

**Contribution.** A flight-load-driven, experimentally validated design workflow for composite UAV structures, plus a dataset of measured fatigue results.

**Fit.** It uses your UAV, CAD and machining skills and your stated interests in generative design and lightweight composites.

## Proposal B, for Dr. Pasini: Defect-aware robust topology optimization of additively manufactured lattice structures for vibrating, impact-loaded UAV components

**Gap.** Pasini and Guest's review ✅ (*MRS Bulletin*, 2019, DOI 10.1557/mrs.2019.231) establishes that manufacturing defects strongly degrade lattice response and reviews topology optimization that accounts for imperfections. His group also co-authored a 2025 design-led defect-compensation framework for laser-powder-bed-fusion truss lattices ✅ (*Journal of Intelligent Manufacturing*, DOI 10.1007/s10845-025-02667-5). ⚠️ I did not find work that applies defect-aware optimization to a UAV component under combined vibration and impact. The proposed gap is that application, with experimental validation.

**Research questions.**

1. Which defect classes (strut waviness, thickness variation, porosity) most affect lattice-filled UAV arms or landing-gear parts?
2. How much does a robust design lose in nominal stiffness and gain in worst-case performance?

**Method.** Characterise as-built defects of printed lattice coupons, model them, run robust optimization, then test printed parts under vibration and impact.

**Contribution.** Design rules for flaw-tolerant lightweight UAV parts.

**Note.** This is the most mathematically demanding of the proposals. Plan to build your FEA and optimization skills before applying.

## Proposal C, for Dr. Suleman: Manufacturing-aware multidisciplinary design optimization of a small multirotor or VTOL UAV, validated by flight test

**Gap.** Reviews of MDO for aerial vehicles ✅ (Papageorgiou et al., *International Journal of Aerospace Engineering*, 2018, DOI 10.1155/2018/4258020) survey practice and gaps. ⚠️ I did not read the full text; check its gaps section. The proposed gap is that manufacturing cost and process limits (machining, printing) are rarely built into the optimization loop for small UAVs that are then flown.

**Research questions.**

1. How does the optimum change when manufacturing constraints are included?
2. Does a surrogate-assisted loop keep that extra fidelity affordable?

**Method.** Parametric CAD, FEA, surrogate-based optimization. Fabricate and flight-test a conventional and a manufacturing-aware variant, and compare endurance and structural mass.

**Contribution.** A reproducible workflow with measured validation. It ties directly to your "UAV design and performance" interest.

## Proposal D, for Dr. Milani: Data-driven multi-criteria design of hybrid or biocomposite UAV structures

**Gap.** Milani's group works on multi-criteria design optimization and machine learning for composites ✅. ⚠️ I did not survey the literature for biocomposite UAV airframes specifically, so treat the gap as a hypothesis: a systematic review is the first deliverable. The question is whether a transparent multi-criteria framework (mass, stiffness, cost, embodied carbon, manufacturability) changes which materials are chosen for small UAV parts.

**Method.** Build a materials and process database from the literature and your own coupon tests, apply multi-criteria decision methods, and validate with one printed or laid-up part.

**Contribution.** A decision tool plus a validated case study, aligned with his "sustainable and smart manufacturing" chair.

## Proposal E, for Dr. Zhang: Early detection and tolerance of ESC and motor-driver faults in multirotors from flight telemetry

**Gap.** UAV fault-diagnosis papers concentrate on propellers and motors, with ESCs mentioned as part of the powertrain: Bondyra et al. (2018, vibration-based blade damage) ✅, Cacace et al. (2024, *Journal of Intelligent & Robotic Systems*, motor-fault isolation with an RNN) ✅, and a 2019 Berkeley study of vibration-based propeller diagnosis ✅. ⚠️ I did not find an ESC-specific review in one search, so run a systematic search before claiming novelty.

**Method.** Build a test rig, inject ESC faults, collect labelled telemetry, and compare model-based residuals with a small learned classifier. Add a fault-tolerant reallocation strategy and validate in controlled flights.

**Contribution.** A labelled ESC-fault dataset and a deployable detector. It builds directly on your ESC diagnostics at Aerotech.

# 5. Verified literature

Entries marked ✅ were confirmed in a source I opened or searched. Cross-check DOIs and exact titles in Google Scholar before citing.

| Citation | Why it matters | Status |
|---|---|---|
| *Generative design of light weight drone frame using FDM 3D printing: a review.* EPJ Web of Conferences, 2026. DOI 10.1051/epjconf/202636701003 | Weight reduction of 20 to 60%; names anisotropy and fatigue as open problems (Proposal A) | ✅ authors not captured |
| Al-Haddad et al. (2024). Quadcopter UAV structural design using an integrated approach of topology optimization and additive manufacturing. *Designs*, 8(3), 58 | Validated by static and impact tests (Proposal A) | ✅ |
| Gandhi, U. and Minak, G. (2022). Review on topology optimization strategies for additively manufactured continuous fibre composites. *Applied Sciences* | Summarises concurrent methods (Proposal A) | ✅ exact title to confirm |
| Mokhtarzadeh, M., López Jiménez, F. and Maute, K. (2024). Concurrent shape and fibre-orientation optimization for continuous-fibre additive manufacturing. *Structural and Multidisciplinary Optimization* | Level-set shape with B-spline fibre fields (Proposal A) | ✅ title approximate |
| Matsuzaki, R. et al. (2016). Three-dimensional printing of continuous-fiber composites by in-nozzle impregnation. *Scientific Reports*. DOI 10.1038/srep23058 | Foundational continuous-fibre printing paper | ✅ |
| Pasini, D. and Guest, J.K. (2019). Imperfect architected materials: mechanics and topology optimization. *MRS Bulletin*. DOI 10.1557/mrs.2019.231 | Defects and flaw-tolerant optimization (Proposal B) | ✅ |
| Murchio, S., Benedetti, M., Dallago, M., Raghavendra, S., Zappini, G. and Pasini, D. (2025). Mitigating manufacturing defects in laser-powder bed fusion: a design-led compensation framework for truss-based metallic lattices. *Journal of Intelligent Manufacturing*. DOI 10.1007/s10845-025-02667-5 | Defect compensation (Proposal B) | ✅ |
| Papageorgiou, A., Tarkian, M., Amadori, K. and Ölvander, J. (2018). Multidisciplinary design optimization of aerial vehicles: a review of recent advancements. *International Journal of Aerospace Engineering*. DOI 10.1155/2018/4258020 | MDO survey (Proposal C) | ✅ |
| Zhang, Y. and Jiang, J. (2008). Bibliographical review on reconfigurable fault-tolerant control systems. *Annual Reviews in Control*, 32(2), 229 to 252. DOI 10.1016/j.arcontrol.2008.03.008 | Foundational review (Proposal E) | ✅ |
| Cacace et al. (2024). Motor fault detection and isolation for UAVs using an external-wrench estimate and an RNN. *Journal of Intelligent & Robotic Systems* | Closest ESC-adjacent work (Proposal E) | ✅ volume and pages not captured |
| Qian, L. and Liu, H.H.T. (2022). Robust path-following control for multiple quadrotors with a slung payload. *Journal of Guidance, Control, and Dynamics*. DOI 10.2514/1.G006173 | Dr. Liu's line of work | ✅ title approximate |
| Chen, T., Shan, J. and Liu, H.H.T. (2022). Rigidly attached payload carried by multiple quadrotors. *International Journal of Aerospace Engineering*. DOI 10.1155/2022/2486561 | Dr. Liu's line of work | ✅ title approximate |
| Yu, Z., Zhang, Y., Jiang, B. and Su, C.-Y. (2023). *Fault-Tolerant Cooperative Control of Unmanned Aerial Vehicles.* Springer. ISBN 978-981-99-7660-7 | Dr. Zhang's recent book | ✅ author order from a retailer |

# 6. Cold emails

**Rules.** Send from your own address, one email per professor, with your CV and a one-page proposal summary attached. Replace each bracketed hook with a specific recent paper from that lab; do not skip this. Keep each email under 200 words.

## Dr. Mehdi Hojjati (Concordia)

**Subject:** MASc inquiry: concurrent topology and fibre-path optimization for 3D-printed composite UAV parts

Dear Professor Hojjati,

I am a First Class B.Eng. Mechanical Engineering graduate (ABUAD, 2025) working as a UAV technician in Lagos. My research interests are lightweight composite structures, generative design and topology optimization, and prototyping.

Your work on composite manufacturing, automated fibre placement and 3D printing, particularly [recent paper], is the closest match I have found to those interests. I am proposing a project on concurrent topology and fibre-path optimization of continuous-fibre printed UAV arms and mounts, driven by loads measured in flight and validated with fatigue and drop tests. A recent review of generative-design drone frames names anisotropy and fatigue as open problems, and I would like to address them experimentally.

Are you considering MASc students for Fall 2027? I would value your advice on fit and funding. My CV and a one-page outline are attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

## Dr. Damiano Pasini (McGill)

**Subject:** MASc inquiry: defect-aware topology optimization of lightweight UAV lattice structures

Dear Professor Pasini,

I am a First Class Mechanical Engineering graduate with hands-on UAV maintenance, CAD and machining experience. I am interested in topology optimization and architected structures for aerospace use.

Your review with James Guest on imperfect architected materials, and your group's work on defect compensation in lattices, frame a question I would like to study: how robust, defect-aware optimization changes the design of lattice-filled UAV components that face vibration and impact. I would characterise as-built defects, optimize, and test printed parts. I know my optimization and FEA skills need to grow, and I am building them now.

Are you accepting MASc students for Fall 2027? CV and outline attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

## Dr. Afzal Suleman (University of Victoria)

**Subject:** MASc inquiry: manufacturing-aware design optimization with UAV flight validation

Dear Professor Suleman,

I am a First Class Mechanical Engineering graduate who designs in Inventor and Fusion 360, machines on lathe and mill, and maintains and flies multirotor UAVs (EASA A1/A3, FAA UAS). Your centre's pairing of multidisciplinary design optimization with subscale flight testing is exactly the environment I want to train in.

I would like to study how including manufacturing constraints (machining and printing limits) in the optimization loop changes the optimum for a small multirotor or VTOL airframe, then build and fly both variants to measure the difference in endurance and structural mass.

Are you taking MASc students for Fall 2027? CV and a one-page outline are attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

## Dr. Abbas Milani (UBC Okanagan)

**Subject:** MASc inquiry: multi-criteria design of hybrid and biocomposite UAV structures

Dear Professor Milani,

I am a First Class Mechanical Engineering graduate with experience in UAV maintenance, machining and CAD. My interests are lightweight composites and smart manufacturing.

Your work on multi-criteria design optimization of composite and biocomposite structures, and your chair in sustainable and smart manufacturing, fit a project I would like to propose: a data-driven framework to choose and validate materials for small UAV structures on mass, stiffness, cost, embodied carbon and manufacturability, demonstrated with one built part.

Are you recruiting MASc students for Fall 2027? CV and a one-page outline are attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

## Dr. Youmin Zhang (Concordia)

**Subject:** MASc inquiry: ESC and motor-driver fault diagnosis for multirotors

Dear Professor Zhang,

I am a First Class B.Eng. Mechanical Engineering graduate and a UAV technician who diagnoses ESC and structural faults on multirotors and FPV drones (EASA A1/A3, FAA UAS).

Your work on fault diagnosis and fault-tolerant control for UAVs, especially [paper or testbed work], matches what I see in the field. ESC faults are usually treated as part of the powertrain, and I would like to study their early detection from flight-controller telemetry and a tolerance strategy for failure. I can build the test rig myself. I am also interested in composite UAV structures, and I have noticed that Concordia's CIADI covers both areas.

Are you considering MASc students for Fall 2027? CV and a one-page outline are attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

## Dr. Pascal Hubert (McGill), short form

**Subject:** MASc inquiry: composites manufacturing for lightweight UAV structures

Dear Professor Hubert,

I am a First Class Mechanical Engineering graduate and UAV technician with machining and CAD experience, interested in lightweight composite structures and smart manufacturing. Your work on sustainable composites manufacturing and out-of-autoclave processing aligns with my goals, and I would like to propose a project on [composite UAV structure]. Are you accepting MASc students for Fall 2027? CV attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

## Dr. Hugh H.T. Liu (University of Toronto), short form

**Subject:** MASc inquiry: fault-aware cooperative payload transport with quadrotors

Dear Professor Liu,

I am a First Class Mechanical Engineering graduate and UAV technician who diagnoses ESC and structural faults on multirotors. I have read your group's work on multi-quadrotor payload control, notably Qian and Liu (2022), and would like to explore how partial thrust loss on one carrier affects cooperative payload stability and how load could be reallocated. I understand the UAV emphasis requires specific courses. Are you considering MASc students for Fall 2027? CV attached.

Sincerely,
Adedamola Adetola | adetoladamolaayo@gmail.com

# 7. Action plan

1. **This week:** clean or remove the template pages on your portfolio, and make the NSE membership level consistent.
2. **Weeks 1 to 3:** build one documented generative-design and FEA example for a UAV arm, and quantify your drone and grain-grinder projects.
3. **Weeks 2 to 4:** run a systematic literature search for each gap you intend to claim, and keep the search strings.
4. **Weeks 2 to 4:** check each programme's deadline, funding and English requirement, then send the emails in two batches: Hojjati, Pasini, Suleman and Milani first, then Zhang and the reaches.
5. **Apply to Concordia (MASc, with M.Eng. as the safety net) and to at least two other programmes** so that a single refusal does not end the cycle.
