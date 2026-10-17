# Skills Employers Require in ML / Deep Learning / Computer Vision Postings (2025–2026), with Emphasis on New-Grad and Early-Career Roles

Research date: 2026-10-17. Method: web search plus a direct fetch of each posting where possible. Many company career pages (Tesla, Meta, NVIDIA Workday/Eightfold, Unstop) blocked or did not render for the fetch tool. For those postings, details come from search-result summaries or aggregator copies (Simplify, Built In, Zapply, Getro, Revolution, Workopia), and this is flagged in each row. Detail labels: **[F]** means the full posting text was read. **[S]** means details come from a search snippet or aggregator summary only and should be checked before use. Most US big-company new-grad 2026 postings found were already **closed**, because the NCG 2026 cycle ran from about mid-2025 to early 2026.

## 1. Evidence table of real postings, grouped by role type

### Takeaway
I collected 46 postings from 2025–2026: 11 read in full and the rest from snippets or aggregators. #45–46 are weakly sourced. The same pattern appears across every role family. Python and PyTorch are close to universal. C++ separates perception, robotics and edge roles from the rest. CUDA, TensorRT, ONNX and quantisation are usually listed as "preferred" or "stand out" items for new grads but become "required" at mid-level. Publications are preferred, never required, outside PhD-track research roles.

### Cited Findings

#### A. Computer vision / perception engineer (autonomous driving, robotics, defense/space, drones, AR/VR)

| # | Company / title | Level | Date / status | Degree | Required (R) / Preferred (P) skills | Src |
|---|---|---|---|---|---|---|
| 1 | **True Anomaly** – Software Engineer I, Perception (New Grad), Denver/Long Beach | New grad; 3-month temporary engagement with possible conversion | Greenhouse; no date shown; open status unknown | Pursuing or recently completed BS/MS (CS/EE/robotics/aero) | **R:** Python with some C++ (training provided); classical tracking (Kalman filters, data association) *or* DL (PyTorch); linear algebra, probability, coordinate transforms; ability to read and implement ICRA/IROS/CVPR/NeurIPS papers; US citizenship. **P:** EKF/multi-object tracking (MOT); YOLO/Faster R-CNN; camera intrinsics/extrinsics and quaternions; **INT8/FP16 quantisation, ONNX, TensorRT**; OpenCV; sensor fusion coursework; synthetic data (Blender/Unreal); Hungarian/JPDA; Jetson/ROS; camera+IMU/lidar fusion | [F] [Greenhouse](https://job-boards.greenhouse.io/trueanomalyinc/jobs/5221970007) |
| 2 | **Bot Auto** – Algorithm Engineer, Deep Learning & Vision (New Grad), Houston/Bay Area (autonomous trucking) | New grad | Greenhouse; no date shown | BS/MS/PhD, upcoming graduates accepted | **R:** experience training neural nets, with coursework, research, personal projects, open source or internships all counting; Transformers/CNNs/GNNs theory; Python and PyTorch; data structures and algorithms. **P:** 3D CV, online mapping, visual SLAM, prediction; publications at CVPR/ICCV/ECCV/NeurIPS/ICLR/ICRA/IROS; **quantisation, distillation, TensorRT, ONNX, CUDA, C++**; AD or robotics internship | [F] [Greenhouse](https://job-boards.greenhouse.io/botauto/jobs/5371947008) |
| 3 | **Waymo** – ML Engineer, Perception LLM/VLM (PhD, New Grad), Mountain View/SF | Titled "New Grad," but lists 5+ yrs ML experience (contradictory) | Careers page; no date shown | MS or equivalent required; PhD preferred | **R:** LLM/VLM pre-training and continual learning at scale; Python; JAX/TF/PyTorch; training, evaluation and deployment in production. **P:** fine-tuning foundation models for AD/robotics; multimodal data curation and QA; publications at NeurIPS/ICML/CVPR/ICCV/ECCV | [F] [Waymo](https://careers.withwaymo.com/jobs/machine-learning-engineer-perception-llm-vlm-phd-new-grad-mountain-view-california-united-states-san-francisco) |
| 4 | **Waymo** – Perception ML Engineer | Mid | Page returned 404 when fetched, so probably closed | BS in CS or similar | 3+ yrs ML/CV; Python; PyTorch or JAX | [S] [Waymo (404 on fetch)](https://careers.withwaymo.com/jobs/perception-machine-learning-engineer-mountain-view-california-united-states-san-francisco) |
| 5 | **Verkada** – Computer Vision Software Engineer, University Graduate 2026, San Mateo (security cameras) | New grad | About 347 days old in the snippet, so likely closed | Bachelor's | C++ and deep learning; on-site 5 days a week | [S] [Greenhouse](https://job-boards.greenhouse.io/verkada/jobs/5040765007) |
| 6 | **Tesla** – AI Engineer, 3D Computer Vision, Self-Driving | Not stated | tesla.com (403 on fetch) | n/s | Object detection and tracking, pose, depth, panoptic segmentation, 3D reconstruction, visual SLAM, SfM, neural rendering; modern DL | [S] [Tesla](https://www.tesla.com/careers/search/job/3d-computer-vision-engineer-self-driving-229691) |
| 7 | **Tesla** – Computer Vision & AI Software Engineer, Autopilot, Palo Alto | Mid (3+ yrs) | LinkedIn; date unclear, may be old | BS in CS/Physics/EE *or* practical experience | 3+ yrs production C/C++; linear algebra, probability, statistics; state estimation, SLAM, camera calibration and geometry | [S] [LinkedIn](https://www.linkedin.com/jobs/view/computer-vision-ai-software-engineer-autopilot-at-tesla-2842889338) |
| 8 | **Zoox** – Software Engineer, Perception 3D Tracking, Foster City | Mid | Built In | n/s | Joint detection and tracking models; **CUDA** | [S] [Built In](https://builtin.com/job/software-engineer-perception-3d-tracking/8131087) |
| 9 | **Zoox** – Software Engineer, Perception Scene Understanding | Senior | Built In | MS/PhD | DL; production ML pipelines; PyTorch, NumPy | [S] [Built In](https://builtin.com/job/software-engineer-perception/7075338) |
| 10 | **Anduril** – Perception Engineer, Machine Learning, Seattle (defense) | Mid/Senior (5+ yrs) | Posted 2026-06-02; **closed** | BS required; MS/PhD preferred | **R:** Python; production C++ and/or Rust; PyTorch, OpenCV; **quantisation, pruning, TensorRT, ONNX**; classical CV (calibration, homography, multi-view geometry, features); new sensor modalities; CI/CD and ML tests; US citizenship and clearance eligibility. **P:** SLAM; AWS, on-prem GPU, W&B/Flyte/RunAI; synthetic data and sim-to-real; CUDA; publications or open source | [F] [Revolution (Anduril board mirror)](https://jobs.revolution.com/companies/anduril/jobs/81298032-perception-engineer-machine-learning) |
| 11 | **Anduril** – Senior Perception Engineer, C++ (and similar perception listings) | Senior (2–4+ yrs) | Several closed | n/s | C++ on Linux; TensorRT and ONNX deployment; PyTorch/TF; CI testing; Python often only "preferred" | [S] [Revolution](https://jobs.revolution.com/companies/anduril/jobs/42053535-senior-perception-engineer-c) |
| 12 | **Skydio** – Autonomy Software Engineer (drones) | Junior (≥1 yr) | Simplify, updated 2026-10-16, so likely open | n/s | **R:** ≥1 yr production code for autonomous robots; C++ and Python; CV, state estimation, planning, controls or sensor integration; FAA Part 107 encouraged; pay $147k–$210k per the search snippet | [F] [Simplify](https://simplify.jobs/p/6bffabd5-e357-467a-b50d-4f21f976c4c2/Autonomy-Software-Engineer) |
| 13 | **Skydio** – Autonomy Engineer, Deep Learning, San Mateo | Mid | skydio.com | **MS or PhD** | **R:** design, train and deploy DL models; Python and PyTorch; applying research. **P:** C++; CV and multimodal DL; large-scale video/sensor data curation and labeling; synthetic data, **knowledge distillation**, label-efficient learning; low-latency embedded optimisation; **evaluation benchmarks** | [F] [Skydio](https://www.skydio.com/jobs/cc83824e-a1cd-4bc7-9206-7264da9fbd61) |
| 14 | **Skydio** – Senior Autonomy Engineer, Computer Vision | Senior | Ashby | n/s | VO, state estimation, mapping, SLAM; probabilistic inference and 3D geometry; DL; high C++ proficiency; $170k–$278k | [S] [Ashby](https://jobs.ashbyhq.com/skydio/3fbd5cc0-36df-4d21-a88b-04e0932109d6/application) |
| 15 | **Skydio** – Autonomy Engineer Intern, CV/DL (Summer/Fall 2026) | Intern | Jobgether / WTTJ | Enrolled students | C++ and/or Python; PyTorch; interest in CV, planning, controls, 3D graphics; $47–$53/hr | [S] [Jobgether](https://jobgether.com/offer/69d47a73aba5fafceeff0dc2-autonomy-engineer-intern---computer-vision-deep-learning-summer-2026) |
| 16 | **Apple** – Computer Vision / ML Engineer, Apple Vision Pro (AR/VR) | Mid (3+ yrs) | jobs.apple.com, 2025 | MSc/PhD in CV/robotics or comparable industry record | C/C++ and Python; PyTorch; real-time SLAM/relocalisation | [S] [Apple](https://jobs.apple.com/en-us/details/200618260-3401/computer-vision-machine-learning-engineer-apple-vision-pro) |
| 17 | **Apple** – CV role, Video Computer Vision group | Mid (BS + 3 yrs) | Freehire copy | BS | C/C++; **CUDA or other GPGPU**; PyTorch/TF/JAX | [S] [Freehire](https://freehire.me/jobs/computer-vision-and-machine-learning-engineer-apple-mdzyflqu) |
| 18 | **Meta** – Research Engineer, Computer Vision & Robotics | Early-mid (BS + 2 yrs) | metacareers (did not render); some listings expire around Apr 2026 | BS completed before start | 2+ yrs CV or robotics perception; C++ or Python | [S] [Meta](https://www.metacareers.com/profile/job_details/1758813528141938) |
| 19 | **Figure AI** – Perception / CV Software Engineer, Helix (humanoid) | Experienced, years not stated | Removed 2025-08-04 (**closed**) | n/s | **R:** white-box DL understanding (losses, training); probability, optimisation, linear algebra; one of 3D reconstruction, depth, neural rendering, detection, tracking/state estimation, segmentation; pinhole model and epipolar geometry; PyTorch. **P:** CUDA; Spark/Ray/SQL; TensorRT and quantisation; publications | [F] [Built In SF](https://www.builtinsf.com/job/perception-computer-vision-software-engineer/2346784) |
| 20 | **Wayve** – ML Engineer, Synthetic Data | Mid (4+ yrs) | Aggregator, 2026 | n/s | GPU training; cameras and 3D geometry; world-model architectures; Python and PyTorch | [S] [Workopia](https://workopia.io/jobs/98e107040e251611ac70b843a3e2896a) |

#### B. Medical imaging CV

| # | Company / title | Level | Date | Degree | Skills | Src |
|---|---|---|---|---|---|---|
| 21 | **MD Anderson** – Senior ML Engineer, Medical Imaging | Senior | 2026 (1–4 months old in the snippet) | n/s | DICOM workflows; dataset versioning; **distributed training** | [S] [MD Anderson](https://jobs.mdanderson.org/search/jobdetails/senior-machine-learning-engineer---medical-imaging/8e631f1b-b409-46ae-87dc-e862c4991576) |
| 22 | **Intuitive Surgical** – Sr. ML Engineer, Medical Imaging | Senior | 2026 | n/s | Medical imaging ML (requirements per search summary: CT/MRI/DICOM, regulated deployment, ONNX/TensorRT, Kubernetes). Field-to-posting mapping is uncertain | [S] [Intuitive](https://careers.intuitive.com/en/jobs/744000131137491/JOB215527/sr-machine-learning-engineer-medical-imaging/) |
| 23 | **University of Luxembourg** – R&D Specialist, AI for Biomedical Imaging | Early-mid | 2026 | n/s | Python, **PyTorch/MONAI** segmentation and detection pipelines; GPU/HPC | [S] [AcademicPositions](https://academicpositions.com/ad/university-of-luxembourg/2026/rd-specialist-in-ai-for-biomedical-imaging/251651) |

#### C. ML engineer / research engineer / applied scientist

| # | Company / title | Level | Date | Degree | Skills | Src |
|---|---|---|---|---|---|---|
| 24 | **Zoox** – Machine Learning Engineer | Senior-leaning | Simplify | MS/PhD | PyTorch, NumPy, Pandas, **vLLM**; production ML pipelines | [S] [Simplify](https://simplify.jobs/p/4a4ac635-d064-4585-8053-2e6065ad4e45/Machine-Learning-Engineer) |
| 25 | **Scale AI** – Staff/Senior ML Research Engineer, Intelligent Systems | Staff (5+ yrs) | Mid-2026 | PhD | SFT, RLHF/RLAIF, reward modelling, eval infrastructure, agents; P: publications or open source; $250k–$350k+ | [S] [Scale](https://scale.com/careers/4714527005) |
| 26 | **NVIDIA** – Research Scientist, Efficient Deep Learning (NCG 2026) | New grad (PhD) | Applications open until at least 2026-06-15, so likely closed now | (PhD track) | Efficient DL (details not retrieved); $168k–$264.5k | [S] via search summary; [NVIDIA search](https://www.indeed.com/q-Nvidia-Deep-Learning-jobs.html) |
| 27 | **Wayve** – Staff MLE, Ops, London | Staff | 2026 | n/s | PyTorch, **TensorRT, quantisation**, deployment; P: MLOps/model registry, CI/CD (GitHub Actions), Grafana | [F] [Workopia](https://workopia.io/jobs/d1e31aa5462bd30c85a20677328c9a50) |
| 28 | **Wayve** – Staff ML Software Engineer, Wayve Labs, Sunnyvale | Staff | 2026 | n/s | Large-scale ML workloads; testing; P: **distributed training**, robotics/sim data | [S] [Dreamwork](https://www.dreamworkhq.com/job/b833fd66-b8ee-4ba8-996e-3c43cc4f2e56) |

#### D. ML infrastructure / inference / performance engineer (mostly NVIDIA NCG)

| # | Company / title | Level | Date / status | Degree | Skills | Src |
|---|---|---|---|---|---|---|
| 29 | **NVIDIA** – AI Software Engineer, LLM Inference Performance Analysis, NCG 2026 | New grad | Accepting applications until at least 2026-01-18; **closed** | **MS or PhD** (or equivalent) | **R:** C++ and Python; transformers/LLM basics; compiler concepts (IR, graph transforms, codegen); one of TensorRT-LLM / PyTorch / JAX-XLA / **Triton** / **vLLM**; bottleneck analysis; class projects, internships, research or **open source** on perf-critical systems. **Stand out:** **CUDA**; agentic AI tools; LLVM/MLIR community | [F] [AnitaB board](https://jobs.anitab.org/companies/nvidia/jobs/65287558-ai-software-engineer-llm-inference-performance-analysis-new-college-grad-2026) |
| 30 | **NVIDIA** – Deep Learning Software Engineer, Inference, NCG 2026 (US remote) | New grad | Open until at least 2026-07-26; now "filled or expired" | Pursuing or completed MS/PhD (search summary) | LLM and GenAI inference performance tuning; $124k–$241.5k | [S] [Workday](https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Deep-Learning-Software-Engineer--Inference---New-College-Grad-2026_JR2021742); [remotejobs.org (expired)](https://remotejobs.org/remote-jobs/deep-learning-software-engineer-inference-new-college-grad-2026-nvidia) |
| 31 | **NVIDIA** – AI Inference Performance Engineer, NCG 2026 | New grad | Status unclear | n/s | Work inside **TensorRT-LLM, SGLang, vLLM**; profiling across CUDA kernels, frameworks and serving layers | [S] [NVIDIA](https://jobs.nvidia.com/careers/job/893393884394) |
| 32 | **NVIDIA** – Developer Technology Engineer, AI, NCG 2026, Santa Clara | New grad | NVIDIA page says no longer accepting applications | n/s | L1 $108k–$178k / L2 $124k–$195.5k (details not retrieved) | [S] [NVIDIA](https://jobs.nvidia.com/careers/job/893393807738) |
| 33 | **NVIDIA** – Software Engineer, DL Kernel Libraries, NCG **2027** | New grad (next cycle) | Open (2027 cohort) | n/s | cuDNN, **FlashInfer** kernel development | [S] [Zapply](https://zapply.jobs/jobs/a38efbc8-c595-4975-b2b8-b41d3433f223/) |
| 34 | **Tesla** – Software Engineer, Generalist, AI Inference (Autopilot and Optimus) | n/s | tesla.com (403) | n/s | Python, modern C++, **PyTorch, CUDA**; deployment on Tesla's in-house AI ASIC | [S] [Tesla](https://www.tesla.com/careers/search/job/software-engineer-generalist-ai-inference--221961) |

#### E. Edge-AI / embedded ML (including India)

| # | Company / title | Level | Date | Degree | Skills | Src |
|---|---|---|---|---|---|---|
| 35 | **Qualcomm** – AI/ML Engineer (XR), Bengaluru | Early-mid | About 420 days old, so likely closed | n/s | Real-time inference on embedded/edge; latency, power and memory optimisation; TF/PyTorch/**ONNX** | [S] [Unstop](https://unstop.com/jobs/aiml-engineer-qualcomm-1545702) |
| 36 | **Qualcomm** – Engineer, AI & ML Systems, Hyderabad | Early (BTech/MTech + 1 yr) | Deadline 2026-06-17 | BTech/MTech | AI/ML software platforms | [S] [beBee](https://bebee.com/in/jobs/engineer-ai-ml-systems-qualcomm-hyderabad-telangana--theirstack-665774217) |
| 37 | **Qualcomm** – Senior Staff/Manager, AI-Embedded C++/ML, Hyderabad | Senior | About 169 days old | n/s | Qualcomm AI Runtime; on-device GenAI on Snapdragon; large C/C++ stacks | [S] [Indeed India](https://in.indeed.com/viewjob?jk=9373b3d3cbc003ba) |
| 38 | **Qualcomm** – AI/ML Performance Engineer (off-campus 2026), Bangalore | Fresher | 2026 (aggregator only) | n/s | Optimising ML workloads on NPU/NSP/GPU; ₹7–9 LPA per the aggregator (unverified) | [S] [job4freshers](https://job4freshers.co.in/qualcomm-ai-ml-engineer/) |
| 39 | **NVIDIA India** – System Software Engineer, GPU, NCG 2026, Pune | New grad | **Closed** | (aggregators: BE/BTech/ME/MTech) | Agentic AI and LLM-based deployment tooling | [S] [NVIDIA](https://jobs.nvidia.com/careers/job/893394324690?domain=nvidia.com&hl=en) |
| 40 | **Recrew AI** – Computer Vision Engineer, Bangalore | **Fresher (0–2 yrs)** | Posted **2026-10-16**, so likely open | BS/MS (Electronics, Physics, Data Science, Astronomy) | **R:** Python OOP; image processing and ML; CNNs for detection/classification; PyTorch and TF/Keras (coursework or personal projects acceptable); SciPy/scikit-learn/Astropy. **P:** OpenCV; Bayesian methods; **Git**; satellite imaging projects. ₹6–8 LPA | [F] [jobfound](https://jobfound.org/job/recrew-ai-is-hiring-for-computer-vision-engineer-bangalore-urban-karnataka-india-india-16-october-2026) |

#### F. Robotics learning / VLA / humanoids

| # | Company / title | Level | Date / status | Degree | Skills | Src |
|---|---|---|---|---|---|---|
| 41 | **Physical Intelligence** – Robotics Research Engineer, SF | n/s | Posted 6+ months ago (Apr 2026 per snippet); **closed** | n/s | Training ML models for robot control, validated on real robots; robotics stack (controls, runtime, perception, state estimation, SLAM, hardware bring-up); data pipelines, training systems, **evaluation frameworks**; research-to-implementation | [F] [Getro](https://s32.getro.com/companies/physical-intelligence/jobs/74211231-robotics-research-engineer) |
| 42 | **Tesla** – AI Engineer, Manipulation, Optimus | n/s | tesla.com (403) | n/s | Production C++ or Python; **imitation learning / RL**; vision-based sensors | [S] [Tesla](https://www.tesla.com/careers/search/job/deep-learning-manipulation-engineer-optimus-224501) |
| 43 | **Wayve** – Staff ML Scientist/Engineer, MEGA team | Staff | 2026 | PhD/MS | **VLA models**, imitation learning, RL; robot foundation models | [S] [Dreamwork](https://www.dreamworkhq.com/job/8ee091ff-e8f8-4bfa-8c3b-af201204692d) |
| 44 | **Physical Intelligence** – Research Scientist, Robot Learning | Research | No closing date | n/s | Foundation-model research; systems on real robots | [S] [researchjobs.in](https://researchjobs.in/job/research-scientist-robot-learning-at-physical-intelligence-san-francisco/) |

#### G. "AI engineer" / LLM applications (new grad)

| # | Company / title | Level | Date | Degree | Skills | Src |
|---|---|---|---|---|---|---|
| 45 | **Quora (Poe)** – new-grad AI/ML role | New grad (2025 or Summer 2026 grads) | **Closed** | n/s | Python or TypeScript; ML math; prior LLM-app or transformer experience | [S] [jobright](https://jobright.ai/jobs/info/69b5f2293b74eb1e2c83a9b7) (source URL attribution uncertain) |
| 46 | **Notion** – new-grad SWE (AI) | New grad | Unclear | Pursuing BS/MS | LLM and embeddings features; Python/TypeScript/React; internships | [S] (search summary only; exact URL not confirmed) |

### Inferences
- The new-grad postings that are genuinely open to bachelor's candidates (True Anomaly, Bot Auto, Verkada, Recrew AI, Skydio interns, and arguably Skydio's junior Autonomy SWE) are mostly at **mid-size or startup companies**. The large-company "New Grad" titles in this set (Waymo VLM, NVIDIA inference, Skydio DL) require an **MS/PhD**, and the Waymo one even lists 5+ years of experience. This suggests big-company ML new-grad hiring in 2025–26 skews heavily toward master's and PhD graduates.
- Robotics, perception and defense postings (True Anomaly, Anduril, Skydio, Tesla Autopilot) are the most C++-heavy. LLM, VLM and research-engineer postings are Python plus a framework (PyTorch/JAX).

### Gaps
- Many company pages (Tesla, Meta, NVIDIA Eightfold, Unstop) could not be fetched, so their full required/preferred split is unverified.
- No **Waymo, Tesla, Meta, Apple, Zoox, Wayve, Figure, PI or Scale** posting that is explicitly *bachelor's-level new grad* in ML/CV was found open. Their absence may reflect closed cycles, not a policy.
- Few Indian postings with full text were found. Indian MNC new-grad ML roles (Google/Microsoft/Samsung R&D India) were not covered.
- No dedicated drone/defense new-grad CV posting from Shield AI or similar was searched.

## 2. Skill tally: how often each skill appears

### Takeaway
Across the **11 fully-read postings [F]** (#1, 2, 3, 10, 12, 13, 19, 27, 29, 40, 41), PyTorch (9/11) and Python (8/11 explicitly) top the list. Next come deployment and optimisation (TensorRT 6/11, quantisation/distillation/pruning 6/11), geometry/SLAM/state estimation (6/11) and data curation/evaluation (6/11). C++ is required in 4/11 and preferred in 2/11. Distributed training, diffusion, Gaussian splatting, Kubernetes and MLflow almost never appear in these perception and new-grad postings. Broader Glassdoor-based analyses confirm Python (~72%) and PyTorch (~38–42%) as table stakes for MLE/AI-engineer titles, with MLOps tools in the 5–18% range.

### Cited Findings

**Hand tally across the 11 fully-read postings** (R = required, P = preferred/bonus; postings as cited in Section 1):

| Skill | R | P | Total /11 | Notes |
|---|---|---|---|---|
| PyTorch (incl. "PyTorch/JAX/TF") | 9 | 0 | 9 | Missing only in PI (#41) and the Skydio junior SWE (#12) |
| Python | 8 | 0 | 8 | Figure, PI and Wayve Ops do not state it |
| C++ (or C++/Rust) | 4 (#1 "some exposure", #10, #12, #29) | 2 (#2, #13) | 6 | Robotics/perception/infra only |
| TensorRT (incl. TensorRT-LLM) | 2 (#10, #27) | 4 (#1, #2, #19, #29 option) | 6 | |
| Quantisation / pruning / distillation | 2 (#10, #27) | 4 (#1, #2, #13, #19) | 6 | |
| Multi-view geometry / SLAM / VIO / state estimation / Kalman | 3 (#1 or-clause, #10, #19) | 3 (#2, #12, #41) | 6 | #12 and #41 list it among required-type competencies |
| Data curation / labeling / synthetic data / evaluation | 1 (#41) | 5 (#1, #3, #10, #13, #19) | 6 | |
| Math (linear algebra, probability, optimisation) | 3 (#1, #2, #19) | 0 | 3 | |
| Publications | 0 | 4 (#2, #3, #10, #19) | 4 | Never required |
| CUDA | 0 | 4 (#2, #10, #19, #29) | 4 | |
| ONNX | 1 (#10) | 2 (#1, #2) | 3 | |
| OpenCV / classical CV | 1 (#10) | 2 (#1, #40) | 3 | |
| VLM / LLM / multimodal | 2 (#3, #29) | 2 (#1, #13) | 4 | |
| MLOps / CI/CD | 1 (#10) | 1 (#27) | 2 | |
| JAX | 0 | 2 options (#3, #29) | 2 | Always as an alternative |
| Triton (language), vLLM | 0 | 1 each (#29 option list) | 1 | Infra roles only |
| Cloud (AWS) | 0 | 1 (#10) | 1 | |
| Git | 0 | 1 (#40) | 1 | Usually assumed |
| Robot learning (IL/RL) | 1 (#41) | 0 | 1 | Plus #42 and #43 [S] |
| Distributed training (DDP/FSDP/DeepSpeed) | 0 | 0 | 0 | Appears only in [S] #21, #28 |
| Diffusion, NeRF/Gaussian splatting | 0 | 0 (neural rendering is one option in #19) | ~1 | Tesla 3D CV [S] #6 lists neural rendering |
| Docker / Kubernetes / MLflow | 0 | 0 | 0 | |

Degree requirements in the [F] set: BS acceptable in 4 (#1, #2, #10, #40). MS/PhD required in 3 (#3, #13, #29). Not stated in 4 (#12, #19, #27, #41).

**Published job-skill analyses (supporting the frequency estimates):**
- 365 Data Science, ML engineer postings (Glassdoor US, "over 1,157" listings, article dated 2026-04-23; collection dates not stated): Python ~72%, Java 21%, SQL 18%; **PyTorch 42%, TensorFlow 34%**, scikit-learn 14%; AWS 35%, Azure 21%; **Kubernetes 15%, Docker 12.2%**, SageMaker 5.9%, **MLflow 5.1%**; **computer vision ~14.9%**, NLP ~19.7%, fine-tuning 10%, RAG 7.2%. Degree: **PhD 36.2%, Master's 22.1%, Bachelor's 17.7%**, not mentioned 23.9%. **Entry level (0–2 yrs) only ~3%** of postings — [365 Data Science MLE outlook](https://365datascience.com/career-advice/career-guides/machine-learning-engineer-job-outlook-2025/)
- 365 Data Science, AI engineer postings (903 cleaned Glassdoor US postings): Python 71%; PyTorch 37.7%, TensorFlow 32.9%, **CUDA 6.1%**; **LangChain 10.7%**, Hugging Face 4.8%, LlamaIndex 4.3%; NLP 19.7%, fine-tuning 14.8%, **RAG 13.6%**, agents 10.6%; Kubernetes 17.6%, Docker 15.4%; CV 12.5%. Degree: PhD 28%, MS 24%, BS 24%. Entry level 0–2 yrs 2.5%. The article contradicts itself on its AWS and Azure figures — [365 Data Science AI engineer outlook](https://365datascience.com/career-advice/career-guides/ai-engineer-job-outlook-2025/)
- Lightcast / Stanford AI Index 2026: AI skills appear in **2.5% of all US postings** in 2025 (up 55% YoY). **Python was the most in-demand specialized skill (258,674 postings, up about 30%)**. The agentic-AI cluster rose from 0.06% to 0.23% of postings (about 90k). ChatGPT and chatbot mentions fell. AWS and scalability skills grew fastest over the long term — [Lightcast AI Index 2026](https://lightcast.io/resources/research/stanford-ai-index-2026)
- Lightcast: "artificial intelligence" overtook "machine learning" as the most-requested AI skill cluster for the first time. Data Scientists (3,301) and ML Engineers (2,951) lead GenAI-skill postings — [Lightcast GenAI 2025](https://lightcast.io/resources/blog/the-generative-ai-job-market-2025-data-insights); [Lightcast AI Index 2025](https://lightcast.io/resources/blog/stanford-ai-otj-2025)
- Lightcast "Beyond the Buzz" (July 2025, 1.3B postings): postings with AI skills advertise **28% (~$18k) higher salaries**. 51% of AI-skill postings are outside IT/CS — [Lightcast press release](https://lightcast.io/resources/blog/beyond-the-buzz-press-release-2025-07-23)
- Stack Overflow Developer Survey 2025 (49k+ respondents, 177 countries): 84% use or plan to use AI tools, and only 3% highly trust AI output. I did not retrieve a 2025 PyTorch usage figure — [SO Survey 2025](https://survey.stackoverflow.co/2025/); [technology section](https://survey.stackoverflow.co/2025/technology/)
- Medical imaging postings recurrently name PyTorch/MONAI, DICOM, ONNX/TensorRT, and regulated deployment (GMLP) — see #21–23 above.

### Inferences
- Combining the tallies: for a CV/perception new grad, **Python + PyTorch + solid DL fundamentals + linear algebra/probability** is the floor. **C++** is the single biggest filter between "ML engineer" and "perception/robotics engineer" postings.
- The **deployment cluster** (TensorRT, ONNX, quantisation, CUDA) is the most common *preferred* differentiator for perception and edge roles (5–6 of 11). Its required/preferred split suggests it is a realistic new-grad differentiator, because it shows up as preferred in new-grad postings and as required in mid-level ones (Anduril, Wayve).
- **Distributed training, MLOps (Docker/K8s/MLflow) and serving (vLLM/Triton server)** are infra and LLM-company signals. They rarely appear in perception postings. In the general MLE population they appear in roughly 5–18% of postings (365 Data Science).
- **Diffusion, NeRF and Gaussian splatting** barely appear in requirements (only "neural rendering" as one option, at Tesla and Figure). They work better as project topics than as checkbox skills.

### Gaps
- The tally covers 11 postings and is a convenience sample, not a statistical estimate. The [S] postings were not included in the counts.
- No Lightcast or Indeed breakdown specifically for **computer vision** roles (e.g. % requiring C++ or OpenCV) was found.
- The 365 Data Science figures are from Glassdoor with an unstated collection window, and the "1,000 vs 1,157" sample-size inconsistency is unresolved.
- The Stack Overflow 2025 framework-usage percentages (PyTorch/TensorFlow) were not retrieved.

## 3. Table stakes vs differentiators per role; bachelor's acceptance and the evidence employers ask for

### Takeaway
Table stakes are Python, PyTorch, DL fundamentals and math everywhere, plus C++ for perception and robotics. Differentiators are deployment optimisation (TensorRT, ONNX, quantisation, CUDA), 3D geometry/SLAM, data/eval tooling, and publications. Postings that explicitly accept bachelor's candidates accept **projects, coursework, open source, internships and research** as evidence. Several state this outright (Bot Auto, Recrew AI, NVIDIA).

### Cited Findings
**Per-role summary (built from Section 1 postings):**

| Role | Table stakes (in R of most postings) | Differentiators (P / "stand out") |
|---|---|---|
| CV / perception (AD, drones, defense, space) | Python, PyTorch, C++ (Anduril, Skydio, Tesla, True Anomaly), linear algebra and probability, detection/tracking/segmentation | TensorRT/ONNX/quantisation, CUDA, SLAM/VIO/multi-view geometry, sensor fusion (camera+IMU/lidar), synthetic data, publications — [True Anomaly](https://job-boards.greenhouse.io/trueanomalyinc/jobs/5221970007), [Bot Auto](https://job-boards.greenhouse.io/botauto/jobs/5371947008), [Anduril](https://jobs.revolution.com/companies/anduril/jobs/81298032-perception-engineer-machine-learning), [Figure](https://www.builtinsf.com/job/perception-computer-vision-software-engineer/2346784) |
| AR/VR (Apple Vision Pro) | C/C++, Python, PyTorch, real-time SLAM | CUDA/GPGPU, CVPR/ICCV publications — [Apple](https://jobs.apple.com/en-us/details/200618260-3401/computer-vision-machine-learning-engineer-apple-vision-pro) |
| Medical imaging | Python, PyTorch/MONAI, DICOM, CT/MRI | ONNX/TensorRT, Kubernetes, nnU-Net, regulated deployment — [Luxembourg](https://academicpositions.com/ad/university-of-luxembourg/2026/rd-specialist-in-ai-for-biomedical-imaging/251651), [MD Anderson](https://jobs.mdanderson.org/search/jobdetails/senior-machine-learning-engineer---medical-imaging/8e631f1b-b409-46ae-87dc-e862c4991576) |
| ML engineer / research engineer (VLM, foundation models) | Python, PyTorch/JAX, large-scale training and eval, often MS/PhD | Publications, multimodal data curation, RLHF/post-training — [Waymo](https://careers.withwaymo.com/jobs/machine-learning-engineer-perception-llm-vlm-phd-new-grad-mountain-view-california-united-states-san-francisco), [Scale](https://scale.com/careers/4714527005) |
| ML infra / inference / perf | C++ and Python, transformer basics, one of TensorRT-LLM/vLLM/SGLang/Triton/JAX-XLA, profiling | CUDA, LLVM/MLIR, open-source contributions — [NVIDIA](https://jobs.anitab.org/companies/nvidia/jobs/65287558-ai-software-engineer-llm-inference-performance-analysis-new-college-grad-2026) |
| Edge-AI / embedded | C/C++, ONNX/TF/PyTorch, latency/power/memory optimisation | NPU/NSP knowledge, on-device GenAI — [Qualcomm](https://unstop.com/jobs/aiml-engineer-qualcomm-1545702), [Qualcomm Hyderabad](https://in.indeed.com/viewjob?jk=9373b3d3cbc003ba) |
| Robot learning / VLA | Training policies on real robots, IL/RL, robotics stack | Evaluation frameworks, data pipelines, hardware bring-up — [PI](https://s32.getro.com/companies/physical-intelligence/jobs/74211231-robotics-research-engineer), [Wayve MEGA](https://www.dreamworkhq.com/job/8ee091ff-e8f8-4bfa-8c3b-af201204692d) |
| AI engineer / LLM apps | Python (often TypeScript), LLM/RAG/agents | LangChain (~11% of postings), fine-tuning — [365 DS AI eng](https://365datascience.com/career-advice/career-guides/ai-engineer-job-outlook-2025/) |

**Postings that explicitly accept bachelor's candidates, and the evidence they ask for:**
- True Anomaly: pursuing or recent BS/MS. Asks for coursework in CV and estimation theory "or willingness to learn," and the ability to implement ICRA/CVPR papers. C++ training is provided. US citizens only — [Greenhouse](https://job-boards.greenhouse.io/trueanomalyinc/jobs/5221970007)
- Bot Auto: BS/MS/PhD. Neural-network training experience can come from "coursework, research, personal projects, open-source work, and internships," with emphasis on debugging failing models. Publications are preferred — [Greenhouse](https://job-boards.greenhouse.io/botauto/jobs/5371947008)
- Recrew AI (India): BS/MS, 0–2 yrs. PyTorch/TF via "coursework or personal projects" is acceptable — [jobfound](https://jobfound.org/job/recrew-ai-is-hiring-for-computer-vision-engineer-bangalore-urban-karnataka-india-india-16-october-2026)
- Verkada: bachelor's required, University Grad 2026 — [Greenhouse](https://job-boards.greenhouse.io/verkada/jobs/5040765007) [S]
- Anduril (mid-level): BS is enough, but 5+ yrs are needed. Publications or open source are preferred — [Revolution](https://jobs.revolution.com/companies/anduril/jobs/81298032-perception-engineer-machine-learning)
- Meta RE CV & Robotics: BS plus 2+ yrs. Apple VCV: BS plus 3+ yrs. Tesla Autopilot: BS "or practical experience" — [Meta](https://www.metacareers.com/profile/job_details/1758813528141938), [Freehire/Apple](https://freehire.me/jobs/computer-vision-and-machine-learning-engineer-apple-mdzyflqu), [LinkedIn/Tesla](https://www.linkedin.com/jobs/view/computer-vision-ai-software-engineer-autopilot-at-tesla-2842889338) [S]
- NVIDIA India NCG (aggregators): BE/BTech eligible. The process includes HackerRank online tests and then interviews — [foundit](https://www.foundit.in/career-advice/nvidia-early-talent-programs/), [NVIDIA event](https://nvidia.eightfold.ai/events/candidate?plannedEventId=qZbodKBYK) [S]
- NVIDIA US NCG inference: MS/PhD, but it explicitly accepts "class projects, internships, research, or open-source work" as evidence — [AnitaB](https://jobs.anitab.org/companies/nvidia/jobs/65287558-ai-software-engineer-llm-inference-performance-analysis-new-college-grad-2026)
- Market-wide, only about 17.7% (MLE) and 24% (AI engineer) of postings name a bachelor's as the degree level, versus 36% and 28% naming a PhD. Only about 2.5–3% of postings are explicitly entry level (0–2 yrs) — [365 DS MLE](https://365datascience.com/career-advice/career-guides/machine-learning-engineer-job-outlook-2025/), [365 DS AI eng](https://365datascience.com/career-advice/career-guides/ai-engineer-job-outlook-2025/)
- Skydio requires or strongly encourages FAA Part 107 drone certification within 60 days, an unusual domain-specific credential — [Skydio](https://www.skydio.com/jobs/cc83824e-a1cd-4bc7-9206-7264da9fbd61)
- Defense and space postings (Anduril, True Anomaly) require **US citizenship** or clearance eligibility, which rules them out for most international students — [Anduril](https://jobs.revolution.com/companies/anduril/jobs/81298032-perception-engineer-machine-learning), [True Anomaly](https://job-boards.greenhouse.io/trueanomalyinc/jobs/5221970007)

### Inferences
- For a bachelor's student, the realistic entry points visible in this sample are startup or mid-size perception and robotics new-grad roles, internships (Skydio, Meta), and Indian fresher CV roles. Big-company research and ML new-grad tracks mostly gate on an MS/PhD.
- The most commonly named substitute for experience is concrete projects that train and *debug* models, plus deployment (exporting to ONNX/TensorRT, quantising, running on a Jetson). These hit both the table-stakes and the differentiator rows. Paper implementations (True Anomaly) and open-source contributions to vLLM/SGLang or LLVM (NVIDIA) are the next most named.
- Citizenship and clearance (defense/space) and certifications like Part 107 (drones) are non-skill filters a student should check early.

### Gaps
- No posting stated that competitions (Kaggle etc.) count as evidence. I found no source on whether competition results are valued.
- No quantitative data on what share of *new-grad* (vs all) ML postings accept a bachelor's was found. The 365 Data Science shares cover all levels.
- Indian postings at large MNCs (Google, Microsoft, Samsung, NVIDIA Bangalore) with full requirement text were not retrieved.
