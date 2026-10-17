# Standing Out as a New-Grad ML / DL / CV Candidate, and What ML/CV Interviews Look Like (2025–2026)

Research date: 2026-10-17. About 16 search/fetch calls were made. Labels used: **[DATA]** = survey, aggregate statistics or a documented policy; **[OPINION]** = a practitioner, hiring manager or vendor view; **[REPORT]** = an anonymous candidate self-report (Glassdoor-type); **[PRIOR]** = from the researcher's background knowledge, NOT re-verified in this session (the writer should treat it as unverified or drop it).

Overall caveat: the open web on this topic is dominated by vendor and career-coach blogs, which want to sell courses or mock interviews. I found almost no rigorous survey data on how hiring managers weight portfolio signals for ML/CV new grads. Most of what follows is informed opinion.

---

## Which signals hiring managers value for new grads in ML/CV, and what separates a strong project from a "tutorial clone"?

### Takeaway
The consistent (opinion-level) message for 2024–2026 is to go for depth over breadth: two or three original, end-to-end projects. Each should have real or unusual data, justified trade-offs, measured results, and ideally a deployment or demo, plus the ability to defend every design choice in a deep-dive. Tutorial clones (MNIST/Titanic/Iris, course-template repos, thin API wrappers) are widely described as non-signals. Kaggle, blogs and open source help mainly as *visible proof of work*, not as standalone credentials. I found no hard data that quantifies the relative weight of each signal.

### Cited Findings
**What a strong project looks like (all opinion)**
- [OPINION, vendor/blog, 2025] The core test is whether a candidate can design full ML systems, handle data problems such as imbalance and drift, and tie work to impact. Iris-style classifiers and basic regression "no longer stand out." — [InterviewNode blog](https://www.interviewnode.com/post/ml-engineer-portfolio-projects-that-will-get-you-hired-in-2025); [Medium, AI Analytics Diaries](https://medium.com/ai-analytics-diaries/the-5-machine-learning-projects-that-will-make-your-resume-stand-out-in-2025-3b2801d2de42)
- [OPINION, blog, 2025] Simply calling a hosted model (an API wrapper) "doesn't count" as a portfolio project. The author wants to see adaptation, cost trade-offs, deployment and explainability. Deployment and MLOps evidence (Docker, MLflow, monitoring) is cited as a signal, and an empty README as a red flag. — [Medium, S. Rout](https://medium.com/@santosh.rout.cr7/ml-engineer-portfolio-projects-that-will-get-you-hired-in-2025-d1f2e20d6c79)
- [OPINION, vendor, 2026] Recruiters recognise DataCamp/Coursera project layouts quickly, so candidates should change the problem or domain. MNIST, Titanic and Iris are named as signs that a tutorial was followed. — [Upskillist](https://www.upskillist.com/blog/10-ai-portfolio-examples-impress-recruiters/)
- [OPINION, recruiting vendor] Repos copied from tutorials "with no meaningful changes" signal a lack of initiative. — [Fonzi.ai](https://fonzi.ai/blog/do-recruiters-check-github)
- [OPINION, resume vendor, 2026] Bullets with real metrics (accuracy lift, latency, cost per inference) are what separate candidates. — [ResumeOptimizerPro](https://resumeoptimizerpro.com/blog/machine-learning-engineer-resume-examples)
- [OPINION, recruiting agency] For most entry-level roles, a portfolio of practical work matters more than the degree. Two or three polished end-to-end projects are recommended. — [People in AI](https://www.peopleinai.com/blog/entry-level-machine-learning-jobs)
- [OPINION, practitioner: Yuan Meng, MLE at DoorDash, 2024-10-15] "Nothing is worse than making a random decision without any justifications." Unjustified trade-offs (accuracy vs. latency, buy vs. build) are a major red flag in project deep-dives. This implies a project's value lies in decisions the candidate can defend. — [Yuan Meng, "(Opinionated) Guide to ML Engineer Job Hunting"](https://www.yuan-meng.com/posts/mle_interviews/)
- [OPINION, new-grad guide on Substack] It is easy to list a model you don't fully understand, and interviewers will probe how it works and what data it used. **Caution:** the author's byline is "Kndrej Aarpathy", which looks like a parody of Andrej Karpathy, NOT Karpathy himself. Do not attribute it to Karpathy. — [Substack, "Breaking into ML as a New Grad"](https://kndrej.substack.com/p/breaking-into-ml-as-a-new-grad)
- [OPINION, Eugene Yan via Daniel Bourke] "Going off the happy path": course code usually works, while your own projects expose the errors that teach most and make you stand out. — [mrdbourke.com](https://www.mrdbourke.com/get-a-machine-learning-job/). Yan in The Batch: use each project to push beyond your comfort zone (e.g., Spark/Dask instead of pandas). — [DeepLearning.AI The Batch](https://www.deeplearning.ai/the-batch/how-to-keep-up-in-a-changing-field/). A TDS interview with Yan is titled "To Turbocharge Your Learning, Pick Hard Projects" (body not retrieved). — [Towards Data Science](https://towardsdatascience.com/to-turbocharge-your-learning-pick-hard-projects-c0943d1fe27d)

**Technical blogs**
- [OPINION, Rachel Thomas, fast.ai, 2017-12-18, dated but still widely cited] Blogging is "like a resume, only better." "I know of a few people who have had blog posts lead to job offers!" She also says personal branding "is no substitute for doing high-quality technical work; it's just the means by which you can share this work with a broader audience." — [fast.ai, "Making Peace with Personal Branding"](https://www.fast.ai/posts/2017-12-18-personal-brand.html)

**Kaggle / competitions**
- [DATA, cited secondhand] Kaggle had over 29 million users and $3.668M in prize money in 2025, per ML Contests' 2025 landscape report, as cited by a training vendor that argues Kaggle "remains worth it" because public notebooks show code quality and communication, not just rank. — [Refonte Learning, 2026](https://www.refontelearning.com/blog/best-kaggle-competitions-for-beginners-2026) (vendor; conflict of interest)
- [OPINION] Some companies (Facebook, Airbnb, Walmart) historically ran Kaggle recruiting competitions where winners got interviews. Kaggle is described as one input, "not a decisive factor." — [GeeksforGeeks](https://www.geeksforgeeks.org/machine-learning/is-kaggle-useful-in-finding-a-machine-learning-job/)
- [WEAK SIGNAL] Blind threads are divided on whether decent Kaggle ranks helped with offers. — [Blind search](https://www.teamblind.com/search/kaggle)

**Interview format as signal evidence**
- [OPINION, Yuan Meng 2024] MLE loops commonly include a dedicated **Project Deep Dive** round (background, alternatives and trade-offs, challenges, impact, reflection). The portfolio project is therefore interview material, not only resume decoration. — [Yuan Meng](https://www.yuan-meng.com/posts/mle_interviews/)

### Inferences
- A good project is one the candidate can survive a 45-minute deep-dive on: original problem or data, baselines plus ablations, error analysis, measured latency/cost, a deployed demo or reproducible repo, and a clear README. This follows from deep-dive rounds and the "justify every decision" red flag.
- Paper reproductions with ablations probably sit well for research-engineer and applied-scientist roles, since they show the ability to read papers and debug training. I found no 2025–26 source that states this directly (see Gaps).
- For CV specifically, likely differentiators are projects that touch geometry or deployment constraints (edge inference, quantisation, real cameras, calibration). These are rarer than "fine-tune YOLO on a Roboflow dataset", which is the CV equivalent of a tutorial clone. This is an inference from the tutorial-clone critiques plus the geometry-heavy CV interviews below.
- Kaggle's value seems to have shifted from "rank as credential" to "public notebook as work sample". A top finish (gold/master) remains a strong signal in opinion pieces, but mid-table participation is weak.

### Gaps
- No survey (e.g., from a recruiter platform) quantifying how ML hiring managers weight projects vs. open source vs. papers vs. Kaggle for new grads. None found.
- No retrieved first-person 2024–26 statements from Chip Huyen, Vicki Boykis, Karpathy, Sebastian Raschka, Hamel Husain, Lilian Weng, or recruiters at NVIDIA/Meta/Tesla on new-grad portfolios. Searches returned only aggregators. [PRIOR, unverified]: Karpathy's "A Recipe for Training Neural Networks" (2019, karpathy.github.io) and his nanoGPT/"Zero to Hero" material are widely used as from-scratch project templates. Hamel Husain has written about open source and "learning in public". Neither was re-checked here.
- Open-source contributions (PyTorch, Hugging Face, OpenCV, timm): no 2024–26 hiring-manager source was found that quantifies their value. This is widely asserted in community discussion, but uncited here.
- Papers/workshop papers for MLE (vs. research) roles: not found. The DeepMind India pre-doc listing below indicates that "some research experience" is a minimum for research tracks.

---

## What do hiring managers, practitioners and surveys say? (named voices and data)

### Takeaway
The best-sourced practitioner voices retrieved are Yuan Meng (DoorDash MLE, 2024), MLEpath (Head of MLOps at a Series B startup, who claims to have coached 150+ people into big-tech ML jobs, Dec 2024), Rachel Thomas/fast.ai (2017), Eugene Yan (via secondary sources), and Chip Huyen's interview book. Survey data on ML hiring signals is very thin. The one quantitative interview report found (Dataford 2026) comes from a prep vendor.

### Cited Findings
- [OPINION, MLEpath, 2024-12-23] An ML interview is "a *behavior* and *skill* proxy." Hiring "can be, well…slightly arbitrary." Answers that sound like "a Wikipedia page" raise red flags, because interviewers want lived experience. — [MLEpath Substack, "Pass ML Engineer Interviews in 2025"](https://mlepath.substack.com/p/pass-ml-engineer-interviews-in-2025)
- [OPINION, MLEpath, 2025] An insider's guide to landing an ML position in 2025 exists from the same author (not fetched). — [MLEpath](https://mlepath.substack.com/p/mlepath-an-insiders-guide-to-landing)
- [OPINION, Chip Huyen, *Introduction to Machine Learning Interviews* book] The book explains "the interviewers' mindset and what kind of signals they look for." On ML systems design: "Almost all companies I've talked to ask at least a question of this type in their interview process", and these "are the questions that candidates often find to be the hardest." It has 200+ knowledge questions plus a separate set of 30 open-ended ML system design questions. Its TOC covers junior vs. senior roles, "Do I need a Ph.D.?", and internship vs. full-time interviews. The section bodies were not retrieved. Note: the book was written around 2020–21 and is not a 2025 source. — [huyenchip.com/ml-interviews-book](https://huyenchip.com/ml-interviews-book/)
- [DATA, vendor] Dataford's 2026 ML interview report analyses 997 ML questions. It reports a median ML Engineer total compensation of $225K (US-centric), and 26% of questions in data interview topics were rated "hard". — [Dataford ML Report 2026](https://dataford.io/blog/machine-learning-interview-report-2026) (via search snippet; methodology not checked)
- [DATA, secondhand] Interview Query's "State of Interviewing 2025" reports that in-person rounds rose from 24% (2022) to 38% (2025), especially for design and behavioural rounds. It attributes this to AI changing interviews. — [Interview Query](https://interviewquery.com/p/ai-interview-trends-tech-hiring-2025) (from a search snippet; page fetch returned HTTP 429, so this is not verified in full)
- [DATA, community resource] alirezadir's "Machine-Learning-Interviews" GitHub repo is a widely used structured prep guide (coding, ML coding, ML system design, breadth, depth, behavioural). — [GitHub](https://github.com/alirezadir/Machine-Learning-Interviews)

### Inferences
- The shift toward in-person rounds (if the Interview Query figure holds) together with AI-allowed rounds means project depth and live explanation matter more, since polished take-home output is less trustworthy as a signal.

### Gaps
- interviewing.io: no ML-specific 2025 data was found. Its well-known SWE data (e.g., on resumes and pedigree) was not retrieved.
- Indian hiring managers' published views: none found.
- NVIDIA/Tesla/Meta recruiter posts on new-grad ML hiring: none found (LinkedIn content is largely not indexed).

---

## What do ML engineer / CV engineer / research engineer / applied scientist interviews look like, and how has AI-assisted coding changed them?

### Takeaway
The standard 2024–26 MLE loop is: (1) DSA coding at the SWE bar (LeetCode Medium, sometimes Hard), (2) ML coding (implement k-means, logistic regression with gradient descent, attention, metrics, or debug PyTorch), (3) ML system design, (4) ML breadth (fundamentals) and depth (domain), (5) a project deep-dive, and (6) behavioural. CV roles add geometry (camera intrinsics, homography, essential/fundamental matrices, distortion) and pipeline design. Theory depth varies by company size. Meta has run an AI-assisted coding round since Oct 2025, while other firms (Cursor's maker, proctored platforms) ban AI. In-person rounds are reportedly rising.

### Cited Findings
**Loop structure (opinion / practitioner)**
- [OPINION, Yuan Meng, 2024-10] Coding is LeetCode-style at the SWE bar. Meta asks two Mediums in 45 minutes, and most places ask one Hard plus one Medium in an hour. Poor coding "can easily disqualify a candidate." — [Yuan Meng](https://www.yuan-meng.com/posts/mle_interviews/)
- [OPINION, Yuan Meng] ML coding examples: K-means/K-means++, linear/logistic regression via gradient descent, KNN, **multi-headed attention**, matrix multiplication, and metrics (ROC-AUC, PR-AUC, nDCG). Backend-heavy teams (Netflix, Reddit) may ask OOP/CRUD-API problems instead. — [Yuan Meng](https://www.yuan-meng.com/posts/mle_interviews/)
- [OPINION, Yuan Meng] ML system design takes 45–60 minutes and turns a vague business problem into an end-to-end system: "a mini design review for an ML project." ML breadth covers bias-variance, regularisation, backprop, optimisers, and vanishing/exploding gradients. ML depth is domain-specific (NLP: Transformer, BERT/GPT, LoRA/QLoRA, RLHF; RecSys: multi-stage ranking, DCN/DIN). — [Yuan Meng](https://www.yuan-meng.com/posts/mle_interviews/)
- [OPINION, MLEpath, Dec 2024] Five interview types: DSA, ML system design, behavioural, ML fundamentals, and ML coding ("debug a PyTorch snippet or throw together a quick pipeline in scikit-learn"). Big companies may skip theory, while smaller ones may ask you to "teach ML in 45 minutes." Prep advice: on LeetCode, if stuck after "3–5 minutes, peek, then revisit that problem a few days later". Prepare about 8 behavioural stories. Without DL experience, allow "a couple of months to ramp" on PyTorch. — [MLEpath](https://mlepath.substack.com/p/pass-ml-engineer-interviews-in-2025)
- [OPINION, Chip Huyen] ML system design questions are near-universal and rated hardest. Difficulty scales with seniority. — [ML Interviews book](https://huyenchip.com/ml-interviews-book/)

**CV-specific (candidate reports)**
- [REPORT, Glassdoor, Mujin (robotics CV), ~2024] The technical round covered geometric CV fundamentals: Essential vs. Fundamental vs. Homography matrices, camera intrinsics, lens-distortion correction, and how intrinsics change after cropping an image. A design exercise asked candidates to design a pipeline to get an object's pose. One reviewer reported no ML-based CV questions. — [Glassdoor Mujin review RVW94976435](https://www.glassdoor.co.in/Interview/Mujin-Interview-E1097457-RVW94976435.htm); [RVW88346984](https://www.glassdoor.co.in/Interview/Mujin-Interview-E1097457-RVW88346984.htm); [RVW85464609](https://www.glassdoor.com.au/Interview/Mujin-Interview-E1097457-RVW85464609.htm)
- [REPORT, older] A 2019-era Magic Leap report listed SLAM, deep learning and bundle adjustment. — surfaced via [Glassdoor CV interview questions search](https://static.glassdoor.fr/Interview/computer-vision-interview-questions-SRCH_KO0,15_IP79.htm) (old; low weight)

**AI-assisted coding and interview integrity**
- [DATA/POLICY, secondary reporting] Meta began rolling out an "AI-enabled coding interview" in **October 2025**. It is described internally as "a new type of coding interview in which candidates have access to an AI assistant." It replaces one of two coding rounds on the SWE/EM onsite (up to E7/M2), while a classic no-AI coding round remains. It runs 60 minutes in a three-panel CoderPad (files, editor, AI chat). The AI cannot edit files, so the candidate writes all the code. Selectable models reportedly include GPT-4o mini, GPT-5, Claude Haiku/Sonnet/Opus variants, Gemini 2.5 Pro and Llama 4 Maverick. There are three phases: bug-fixing, core implementation (AI expected), and optimisation on larger inputs. It is graded on the same four competencies: problem solving, code quality, verification, and communication. The internal guidance quoted is "Should use AI, but need to show you understand the code." Candidates reported the in-interview AI was less helpful than their own tools. — [Hello Interview blog](https://www.hellointerview.com/blog/meta-ai-enabled-coding); press coverage: [Yahoo News (citing 404 Media/Business Insider)](https://ca.news.yahoo.com/meta-let-job-candidates-ai-160303016.html); [PracHub 2026](https://prachub.com/resources/meta-ai-coding-interview)
  - Uncertainty: the sources are prep vendors and press, not Meta's own published policy. Whether ML-engineer loops (vs. SWE) use the AI round was not confirmed.
- [OPINION/POLICY, secondary] Policies are mixed. Anysphere (Cursor) reportedly bans AI in its first coding round. Proctored platforms (Codility, HireVue) ban AI and monitor camera, screen and browser. Hidden AI use where banned "can get you on a do-not-hire list." — [Wikipedia: Anysphere](https://en.wikipedia.org/wiki/Anysphere); [Mockif](https://mockif.com/coding-interviews-with-ai-allowed); [TechScreen](https://techscreen.app/articles/is-using-ai-during-coding-interview-cheating)
- [CONTEXT] Cluely, the "cheat on everything" interview-assistant startup founded by Roy Lee after the Columbia/Amazon LeetCode cheating controversy, is the emblematic case that pushed companies toward in-person and AI-aware formats. — [Wikipedia: Cluely](https://en.wikipedia.org/wiki/Cluely); [Wikipedia: Roy Lee](https://en.wikipedia.org/wiki/Roy_Lee_(entrepreneur))
- [DATA, secondhand] In-person rounds rose from 24% (2022) to 38% (2025). — [Interview Query](https://interviewquery.com/p/ai-interview-trends-tech-hiring-2025) (snippet only)
- [OPINION] Where AI is permitted, sources say the emphasis is on *how* candidates use it (verification, reading and understanding generated code), not whether they do. — [Mockif](https://mockif.com/coding-interviews-with-ai-allowed); [Hello Interview](https://www.hellointerview.com/blog/meta-ai-enabled-coding)

### Inferences
- For new grads, plan prep across several tracks: LeetCode Medium fluency (still a hard filter); from-scratch NumPy/PyTorch implementations (attention, conv2d, k-means, logistic regression, backprop for an MLP, IoU/NMS/mAP for CV); 1–2 ML system design frameworks; fundamentals flashcards; a rehearsed 45-minute deep-dive on your best project; and roughly 8 STAR stories.
- CV roles split into (a) geometry/robotics/AR-heavy roles (Mujin-type: multi-view geometry, calibration, pose), and (b) DL-perception roles (detection/segmentation metrics, augmentation, architectures). Candidates should check the JD to see which applies.
- Prepare for both kinds of coding round: no-AI live coding and AI-assisted coding. In the latter, practise prompting, reading and verifying AI code, and handling optimisation follow-ups.
- Research-engineer and applied-scientist loops likely add paper discussion and research talks. This is [PRIOR], not sourced here.

### Gaps
- No primary company prep page (Meta/Google/NVIDIA careers sites) was retrieved for ML-specific rounds.
- No source found for detection/segmentation metric questions (mAP, IoU, NMS) or augmentation questions in 2025 CV interviews. These are widely assumed but unsourced here.
- Take-home prevalence in 2025–26 for ML roles: not found (only general reports that AI has made take-homes less trusted).
- Applied scientist (Amazon) and research engineer (DeepMind/OpenAI-type) loop specifics: not retrieved.
- Interviewing.io ML-specific data: none found.

---

## How do Indian candidates get noticed by international and GCC teams?

### Takeaway
The verifiable, structured routes are research programs. These include Google DeepMind India's 2-year Pre-Doctoral Researcher role (Bangalore), the MSR India Research Fellows program (1–2 years, B.Tech/M.Tech grads, often via department nomination), Google Student Researcher roles, and abroad internships like Mitacs Globalink and DAAD WISE. The availability of Mitacs and DAAD WISE for Indian students in 2026 is **disputed** between sources and must be checked on the official pages. I found no sourced evidence on referrals, cold outreach or GCC-specific hiring behaviour.

### Cited Findings
- [DATA, job listing] Google DeepMind India Pre-Doctoral Researcher ("University Graduate, 2025 Starts", fixed-term): 24 months in Bangalore. Pre-docs are expected to publish externally. Minimum requirements are a STEM bachelor's, Python/C++/Java, and some ML/AI research experience. A master's is preferred. A "2026 Starts" cohort listing also exists. — [The Muse listing](https://themuse.com/jobs/google/predoctoral-researcher-university-graduate-2025-starts-fixedterm-contract); [India Jobs mirror](https://jobs.theindiajobs.com/c/Google-Careers/jobs/pre-doctoral-researcher-university-graduate-2025-starts-fixed-term-contract-rbeah5zkyb)
- [DATA, job listing] Google Student Researcher 2026 (for enrolled students). — [Google Careers](https://google.com/about/careers/applications/jobs/results/103667844620657350-student-researcher-2026)
- [DATA, official] MSR India Research Fellows: 1–2 years at MSR India for BS/BE/BTech or MS/ME/MTech CS-related graduates (2026 cycle: graduating by summer 2026). PhD students and graduates are not eligible. Department heads can nominate final-year students (up to 3 per institute). — [Microsoft Research: RF program nominations](https://www.microsoft.com/en-us/research/academic-program/research-fellows-program-at-microsoft-research-india/nominations/); [MSR RF program page](https://www.microsoft.com/en-us/research/?p=622332)
- [DATA, listing] A Microsoft Research Fellow role in the FoSSE team (CoreAI, co-located with MSR India) accepts applications on a rolling basis. It requires a CV plus at least one recommendation letter sent directly by the recommender. — [AnitaB jobs listing](https://jobs.anitab.org/companies/microsoft-2/jobs/90377804-research-fellow)
- [DATA, secondary guides, conflicting] Mitacs Globalink offers a 12-week internship at Canadian universities with a reported stipend of about CAD 4,500. The Indian cohort is reportedly via AICTE (about 300 places a year) and limited to B.E./B.Tech. DAAD WISE is described as for Indian students only, with a stipend of roughly EUR 750–934/month, and requires a German professor's invitation. — [internshipabroad.in (Mitacs)](https://internshipabroad.in/blog/mitacs-globalink-research-internship-2026-indian-students); [internshipabroad.in (DAAD WISE)](https://internshipabroad.in/blog/daad-wise-scholarship-2026-indian-students-germany-internship); [LeapScholar DAAD WISE 2027](https://leapscholar.com/blog/daad-wise-internship-in-germany-for-indian-students/)
  - **Conflict:** one guide says Mitacs Globalink and DAAD WISE were both *suspended* for Indian students in 2026, and that DAAD's own database showed "This programme is not available right now" (Aug 2026). — [IITian Vibes](https://iitianvibes.com/blog/iit-summer-internships-2026-mitacs-daad-shut-and-2027-map/). Other 2027-focused guides still describe both as open (e.g., a Mitacs deadline of 16 Sept 2026). — [LeapScholar research internships](https://leapscholar.com/blog/research-internship/); [LeapScholar global internships](https://leapscholar.com/blog/global-internship-opportunities-for-indian-students/). All of these are secondary education-consultancy blogs.
- [OPINION] Some programs commonly listed for Indian students (RISE Germany, NASA direct internships) are reportedly not actually open to India. — [Karan Gupta guide](https://www.karangupta.com/guides/internship-research-abroad-guide) / [WeMakeScholars](https://www.wemakescholars.com/blog/paid-internships-abroad-for-indian-students) (exactly which guide made this claim is uncertain from the search summary)
- [OPINION, Eugene Yan] Find mentors via friends of friends on LinkedIn and check in on a regular cadence (e.g., quarterly). This is general networking advice, not India-specific. — [The Batch](https://www.deeplearning.ai/the-batch/how-to-keep-up-in-a-changing-field/)
- [OPINION, Chip Huyen book] The appendix includes advice on building your network (contents not retrieved). — [ML Interviews book](https://huyenchip.com/ml-interviews-book/)

### Inferences
- For an Indian new grad targeting research-flavoured ML/CV roles, the MSR India RF and DeepMind India pre-doc programs act as high-signal "bridge" credentials. They yield publications and recommendation letters from known researchers, which then open doors to international PhDs and GCC research teams. Both require prior research experience, which in practice means professor-guided projects or research assistantships during undergrad.
- Because of the Mitacs/DAAD uncertainty, a candidate should not rely on a single abroad-internship program. Direct emails to professors (which DAAD WISE requires anyway) and summer research at IISc/IITs are fallbacks. This is an inference and was not sourced here.
- Open-source work (GSoC with OpenCV, PyTorch, Hugging Face or similar organisations) plausibly gives location-independent, publicly verifiable signal that offsets a lack of brand-name college or internship. This is not sourced here (see Gaps).

### Gaps
- Google Summer of Code: no source retrieved on its 2025–26 role or value for Indian ML/CV candidates. [PRIOR, unverified]: OpenCV, TensorFlow and other ML organisations have historically been GSoC mentoring orgs, and India has been among the top countries by GSoC participant numbers.
- Referrals vs. cold outreach effectiveness for Indian candidates applying to GCCs (Global Capability Centres) or international teams: no data or hiring-manager quotes found.
- Google Research India (now Google DeepMind India) AI Residency/pre-doc acceptance rates: not found.
- Indian GCC hiring-manager opinions on ML/CV new grads (e.g., NVIDIA Bangalore/Pune, Qualcomm Hyderabad, Samsung R&D Bangalore): none found in this session.
