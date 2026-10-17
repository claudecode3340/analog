# Technical Trends in Computer Vision and Deep Learning (2024 to Oct 2026): What CV/ML Engineers Need to Know, and Which Skills Are Commoditised or Scarce

*Notes compiled 2026-10-17. About 19 web searches, mostly secondary coverage. Items marked [PRIMARY-KNOWN] cite well-known primary pages (arXiv, official blogs) that the researcher knew of from before this session and did not re-fetch here. The report writer should treat those as reliable for dates and existence, but not for fine detail. "Opinion" marks an expert or vendor view, not a measured fact.*

---

## 1. Vision foundation models and how companies use them

### Takeaway
Between 2024 and 2025, general-purpose vision backbones (DINOv3, SigLIP 2), promptable segmenters (SAM 2 and SAM 3), and open VLMs (Qwen3-VL, InternVL) became good enough that a frozen backbone plus a small head, or a VLM prompt, now matches or beats many task-specific models. In industry the dominant pattern is to use foundation models as frozen feature extractors and as auto-labellers ("teachers"), then distil into small deployable detectors. Large open VLMs are used for long-tail understanding, OCR and documents, and GUI and video tasks.

### Cited Findings
- **DINOv3 (Meta, Aug 2025):** a self-supervised model trained on 1.7B images, scaled to 7B parameters, with no labelled data. Meta claims that "a single frozen vision backbone outperforms specialized solutions" on dense tasks including detection and semantic segmentation. The release includes ViT and ConvNeXt variants and distilled smaller models on Hugging Face (facebookresearch/dinov3). — [Meta AI blog](https://ai.meta.com/blog/dinov3-self-supervised-vision-model/)
- DINOv3 frozen-feature numbers from a secondary source (unverified): about 84.5% ImageNet-1K top-1, about 63.0 mIoU on ADE20K (ViT-L), about 66.1 COCO mAP. — [Medium summary](https://medium.com/@malikhannan6856/metas-dinov3-resets-the-baseline-for-computer-vision-f59ad4af3826). Treat these numbers with caution.
- **SAM 3 (Meta, 19 Nov 2025):** introduces "Promptable Concept Segmentation". Given a noun phrase (e.g. "yellow school bus") or an image exemplar, it returns masks and IDs for *every* matching instance in images and video. SAM 1 and SAM 2 returned one object per prompt. It ships with the SA-Co benchmark, open checkpoints, and inference and fine-tuning code under the SAM License. It was released alongside **SAM 3D**, which does object and scene reconstruction and human pose and shape estimation. — [Roboflow](https://blog.roboflow.com/what-is-sam3/); [Ultralytics docs](https://docs.ultralytics.com/models/sam-3); [W&B news](https://wandb.ai/byyoung3/ml-news/reports/Meta-Launches-SAM-3-and-SAM-3D--VmlldzoxNTEyMTQyNA)
- Industry tooling integrated SAM 3 quickly: Ultralytics, Roboflow and Voxel51 all have SAM 3 pages or integrations. This is a strong adoption signal for annotation and labelling workflows. — [Voxel51](https://voxel51.com/glossary/sam-3-segment-anything-model-3); [Ultralytics](https://docs.ultralytics.com/models/sam-3)
- **SigLIP 2 (Google, early 2025):** released in four sizes (ViT-B/86M, L/303M, So400m/400M, g/1B). It extends the SigLIP objective with a unified recipe and is widely used as the vision encoder inside VLMs. — [Superlinked model page](https://www.superlinked.com/models/google-siglip2-base-patch16-224.md)
- **Depth Anything 3 (ByteDance Seed, 14 Nov 2025):** uses a single plain transformer (DINO-style encoder) as backbone. It is already offered in the Roboflow playground. — [Roboflow](https://blog.roboflow.com/depth-anything-3/)
- **Qwen3-VL (Alibaba, 23 Sep 2025):** an Apache-2.0 open-weight family ranging from 2B to 235B-A22B MoE, with 256K native context (extensible to 1M). It does GUI interaction, screenshot-to-code, analysis of video up to about 2 hours, and OCR in 32 languages. Alibaba claims the Instruct model matches or beats Gemini 2.5 Pro on major perception benchmarks. Simon Willison noted these are "a flurry of self-reported benchmarks". — [The Decoder](https://the-decoder.com/open-source-qwen3-vl-outperforms-gemini-2-5-pro-in-major-vision-benchmarks-alibaba-reports/); [Simon Willison](https://simonwillison.net/2025/Sep/23/qwen3-vl)
- **Usage pattern (frozen backbone, then distil):** Roboflow's Autodistill (since June 2023) uses a large base model such as Grounding DINO to label images from text prompts, then trains a small target model such as YOLOv8. Roboflow now sells hosted "Auto Label". — [Roboflow blog](https://blog.roboflow.com/autodistill/); [Roboflow auto-labelling](https://blog.roboflow.com/automated-image-labeling/)

### Inferences
- The "foundation model" layer of CV has consolidated around a small number of open releases from Meta (DINO, SAM, V-JEPA), Google (SigLIP, PaliGemma), Alibaba (Qwen-VL), Shanghai AI Lab (InternVL) and ByteDance (Depth Anything). Most practitioners now *consume* these models rather than train backbones.
- The value-adding work has shifted to choosing the right backbone, adapting it cheaply (linear probes, LoRA, adapters), distilling it into something that meets a latency budget, and validating it on in-domain data.
- Frontier closed VLMs (Gemini, GPT) and open VLMs (Qwen3-VL) make zero-shot "describe, classify or extract" tasks trivially accessible. That erodes demand for bespoke classifiers in low-volume, long-tail applications. High-volume, latency-bound or edge applications still need small specialised models.

### Gaps
- No primary data was found on the *share* of companies using frozen backbones vs full fine-tuning vs distillation. Evidence is anecdotal or comes from vendors (Roboflow, Ultralytics).
- No 2025–2026 sources were fetched on Florence-2, Grounding DINO successors, PaliGemma 2, Llama vision or InternVL3. Their status is not verified here.
- The DINOv3 licence terms were not verified.

---

## 2. World models and embodied AI (VLAs, humanoids) and hiring momentum

### Takeaway
2025 was the breakout year for "physical AI". Interactive world models arrived (Genie 3, Aug 2025), as did open world foundation models (NVIDIA Cosmos, Jan to Mar 2025) and self-supervised video world models used for planning (V-JEPA 2, Jun 2025). Vision-language-action (VLA) models proliferated (π0 to π0.7, GR00T N1, Gemini Robotics 1.5). Capital is very high: humanoid VC reached $8.7B in 2026 YTD by July, almost double 2025's record. Real deployment at scale is still limited, and hiring is concentrated in a small number of well-funded labs.

### Cited Findings
- **Genie 3 (Google DeepMind, 5 Aug 2025):** a general-purpose world model that generates interactive 3D environments from text. It runs in real time at 24 fps and 720p, stays consistent for "a few minutes", and supports "promptable world events". DeepMind's SIMA agent completed goal-directed tasks inside it. It was a limited research preview. — [TechCrunch](https://techcrunch.com/2025/08/05/deepmind-reveals-genie-3-a-world-model-that-could-be-the-key-to-reaching-agi); [TechRadar](https://www.techradar.com/ai-platforms-assistants/watch-this-google-genie-3-can-create-a-3d-world-let-you-explore-it-and-interact-with-it-in-real-time)
- **V-JEPA 2 (Meta, Jun 2025):** a JEPA encoder and predictor pretrained on more than 1M hours of unlabelled video. The action-conditioned variant V-JEPA 2-AC was fine-tuned on about 62 h of DROID robot video (eWeek says 6 h; most sources say 62) and achieves zero-shot pick-and-place planning on Franka arms by CEM planning toward a goal image. It scores 77.3% on SSv2. — [LearnOpenCV](https://learnopencv.com/v-jepa-2-meta-world-model-robotics-guide/); [W&B](https://wandb.ai/byyoung3/ml-news/reports/Meta-Unveils-V-JEPA-2-A-World-Model-for-Physical-Understanding-Prediction-and-Robot-Planning--VmlldzoxMzE4Mjc2Mw); [eWeek](https://www.eweek.com/news/meta-vjepa-2-world-model-ai/)
- **NVIDIA Cosmos and GR00T (GTC, Mar 2025):** the Cosmos world foundation models are Transfer (structured inputs such as depth or lidar to photoreal video, used for synthetic data), Predict (future frames) and Reason (CoT). **Isaac GR00T N1** is an open humanoid foundation model (GR00T-N1-2B on Hugging Face) with a dual-system design: a slow VLM planner and a fast action module. — [Hugging Face/NVIDIA blog](https://www.huggingface.co/blog/nvidia-physical-ai); [Hackster](https://www.hackster.io/news/nvidia-isaac-groot-n1-is-an-open-source-foundation-model-for-accelerated-humanoid-robot-development-effa04c90231)
- 2026 updates, less verified: Cosmos Predict 2.5 (2B and 14B, Apache 2.0 code with NVIDIA Open Model License weights) — [CGWorld](https://cgworld.jp/flashnews/01-202601-NVIDIA-Cosmos.html). GR00T N1.7 reportedly shipped in Mar 2026, and GR00T N2 with world-model capabilities was previewed at GTC 2026 — [Metavert (secondary)](https://metavert.io/nvidia-isaac). **Unverified; confirm with NVIDIA.**
- **Physical Intelligence:** model line π0, π0.5, π0.6, π0.7 (camera plus language to arm and gripper actions). It positions itself as a software layer, not a robot maker. It raised $400M in 2024 at about $2.4B (CNBC) or $2B (Reuters). Later rounds reportedly put it near $5.6B (Nov 2025), with roughly $2.1B raised in total. A ~$1.05B round appears in filings from May 2026 (secondary sources; approximate). Interviews focus on VLA modelling and imitation learning. — [Pulse 2.0](https://pulse2.com/physical-intelligence-raises-400-million-at-2-4-billion-valuation-to-develop-ai-for-robotics); [RevenueMemo](https://www.revenuememo.com/p/physical-intelligence-funding); [TechInterview guide](https://www.techinterview.org/post/3233477140/physical-intelligence-interview-guide/)
- **Humanoid capital:** humanoid VC was $8.7B in 2026 YTD as of 22 Jul, nearly double 2025's full-year record. China accounts for about two-thirds of 2026 humanoid funding and the US for 15%. Neura Robotics raised a $1.4B Series C. — [Dealroom](https://dealroom.co/charts/humanoid-robotics). Figure AI raised more than $1B in its Series C at a $39B post-money valuation (16 Sep 2025) — [via Dealroom/aggregators](https://dealroom.co/charts/humanoid-robotics). Humanoid (London) raised a $152M Series A at $1.35B — [Ground News](https://ground.news/article/humanoid-raises-152-million-at-135-billion-valuation-europes-newest-robot-unicorn). 2025 totals conflict: $3.2B vs more than $3.7B across 26 rounds — [ai2.work](https://ai2.work/blog/how-robotics-funding-entered-its-billion-dollar-mega-round-era).
- **State of AI Report 2025 (Air Street, Oct 2025)**, via secondary summaries: it names world models (e.g. Genie 3) as an emerging area and highlights "reason-before-acting" robotics (Gemini Robotics 1.5, AI2 MolmoAct). Its headline is that 2025 is the start of AI's "industrial era", with bottlenecks shifting to capital, politics and physics. — [DeepLearning.AI The Batch](https://www.deeplearning.ai/the-batch/the-state-of-ai-report-2025-says-ais-barriers-arent-technological-but-social-and-material); [Quasa summary](https://quasa.io/media/state-of-ai-report-2025-key-highlights); [stateof.ai](https://www.stateof.ai/2025-report-launch)
- **Autonomous driving has converged on end-to-end learning:** Tesla dropped its modular code for an end-to-end architecture. Wayve trains a single transformer foundation model with no HD maps. Wayve raised $1.2B from NVIDIA, Uber and three automakers in Feb 2026. One analysis claims Waymo also now uses an end-to-end-trained foundation model, but this is disputed. — [Understanding AI](https://www.understandingai.org/p/waymo-and-teslas-self-driving-systems); [TechCrunch Feb 2026](https://techcrunch.com/2026/02/24/self-driving-tech-startup-wayve-raises-1-2b-from-nvidia-uber-and-three-automakers)
- Earlier VLA lineage, for context [PRIMARY-KNOWN]: RT-2 (Google DeepMind, Jul 2023) — [arXiv 2307.15818](https://arxiv.org/abs/2307.15818). OpenVLA (7B open VLA, Jun 2024) — [arXiv 2406.09246](https://arxiv.org/abs/2406.09246). π0 (Physical Intelligence, Oct 2024) — [arXiv 2410.24164](https://arxiv.org/abs/2410.24164).

### Inferences
- Hiring momentum is real but narrow. Huge rounds flow to a few dozen companies (Figure, Physical Intelligence, Neura, Wayve, plus Chinese humanoid makers). They hire people who combine vision, policy learning, data collection and teleoperation infrastructure, and real-robot integration. These are scarce profiles. Generic "CV engineer" roles benefit less directly.
- The heavy concentration of humanoid capital in China (about 2/3) is important for location strategy.
- Research hype exceeds deployment. Genie 3 is a preview. V-JEPA 2 planning covers simple pick-and-place. VLAs remain mostly in pilots. Treat timelines as uncertain.

### Gaps
- No quantitative data was found on robotics or embodied-AI job postings (counts, growth) or salaries. Gemini Robotics 1.5 and Tesla Optimus hiring were not covered in the results.
- No primary text of the State of AI 2025 was fetched. Its job and talent slides are not covered.
- π0.5 technical details (open-world generalisation, Apr 2025) were not verified in this session.

---

## 3. 3D vision: NeRF to Gaussian splatting, feed-forward reconstruction, SLAM, classical geometry

### Takeaway
3D Gaussian splatting (3DGS) displaced NeRF as the practical representation and is now being standardised in glTF (2025–2026). Learned feed-forward reconstruction (DUSt3R/MASt3R, then VGGT, which won CVPR 2025 Best Paper) replaces parts of the classical SfM/MVS pipeline. That makes *geometry literacy combined with learning* more valuable, while hand-tuning classical pipelines in isolation becomes less valuable.

### Cited Findings
- **VGGT (Oxford VGG and Meta AI, CVPR 2025 Best Paper):** a single feed-forward transformer infers camera parameters, point maps, depth maps and 3D point tracks from 1 to hundreds of views in under a second. Its successor **VGGT-Ω** is a CVPR 2026 oral and best-paper finalist. The VGGT-Ω authors flag possible benchmark contamination in an ancestor checkpoint of the released 1B model. — [CVF Open Access](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_VGGT_Visual_Geometry_Grounded_Transformer_CVPR_2025_paper.html); [arXiv 2503.11651](https://arxiv.org/abs/2503.11651v1); [CVPR 2025 Awards](https://cvpr.thecvf.com/Conferences/2025/News/Awards_Press); [LearnOpenCV VGGT-Ω guide](https://learnopencv.com/vggt-vs-vggt-%cf%89-vggt-omega-a-complete-guide-to-feed-forward-3d-reconstruction/)
- Production-oriented work already exists: a TensorRT-optimised VGGT reconstructs from 5 images in about 62 ms. — [Towards AI](https://towardsai.com/p/machine-learning/vggt-5-images-%E2%86%92-3d-in-62ms-tensorrt-optimization-for-cvpr-2025-best-paper)
- Voxel51 characterises VGGT as "a pure neural approach to 3D vision" (opinion or framing). — [Voxel51](https://voxel51.com/blog/vggt-is-a-pure-neural-approach-to-3d-vision)
- **Gaussian splatting standardisation:** Khronos, OGC, Niantic Spatial, Cesium (Bentley) and Esri are bringing splats into glTF (announced around SIGGRAPH, Aug 2025). Niantic's SPZ format (MIT licence) compresses splats by up to 90% vs PLY. The KHR_gaussian_splatting release candidate came out on 3 Feb 2026. — [Khronos blog](https://www.khronos.org/blog/have-gaussian-splats-arrived-in-the-standardization-sweet-spot); [CGPress](https://cgpress.org/archives/khronos-and-ogc-developing-3d-gaussian-splats-for-gltf-standard.html); [Informed Infrastructure](https://informedinfrastructure.com/post/khronos-announces-gltf-gaussian-splatting-extension)
- Meta's SAM 3D (Nov 2025) brings single-image object and human 3D reconstruction into a mainstream release. — [W&B](https://wandb.ai/byyoung3/ml-news/reports/Meta-Launches-SAM-3-and-SAM-3D--VmlldzoxNTEyMTQyNA)
- Original references [PRIMARY-KNOWN]: 3DGS (Kerbl et al., SIGGRAPH 2023) — [arXiv 2308.04079](https://arxiv.org/abs/2308.04079). DUSt3R (Naver Labs, CVPR 2024) — [arXiv 2312.14132](https://arxiv.org/abs/2312.14132).

### Inferences
- When geospatial and graphics standards bodies standardise a format, that signals industrial adoption rather than research hype. This applies to digital twins, GIS (Esri, Cesium), AR (Niantic) and e-commerce.
- Classical multi-view geometry (Szeliski or Hartley–Zisserman level) remains durable. You need it to understand and evaluate feed-forward models, to debug calibration and scale, to fuse outputs with SLAM and sensors, and to catch failure modes such as the contamination VGGT-Ω flagged. Writing bespoke SfM pipelines from scratch is less of a differentiator.
- SLAM in industry (robotics, AR, AV) is increasingly a hybrid of learned front-ends and classical back-ends (bundle adjustment, factor graphs). This is an inference; no source was fetched on it.

### Gaps
- No sources on SLAM industry practice in 2025–2026 (e.g. MASt3R-SLAM adoption, Apple, Meta AR) were retrieved.
- No hiring data specific to 3D or splatting roles.
- Google Maps' use of splatting was not confirmed.

---

## 4. Generative vision: diffusion, flow matching, video generation

### Takeaway
Flow matching and diffusion transformers are now the standard architecture for image and video generation. Strong open-weight video models (e.g. Wan 2.2, Apache 2.0, MoE flow matching) coexist with closed frontier models (Veo 3, Sora 2 with synchronised audio). Demand for engineers who can *train or serve* these models is concentrated at labs and media-tech firms. Using them through APIs is commoditised.

### Cited Findings
- **Wan 2.2 (Alibaba, Jul 2025):** open weights (Apache 2.0) using a novel MoE flow-matching architecture, with one expert for high-noise steps and one for low-noise steps. The 5B TI2V model runs on consumer GPUs. — [DeepLearning.AI The Batch](https://charonhub.deeplearning.ai/alibabas-wan-2-2-video-models-adopt-a-new-architecture-to-sort-noisy-from-less-noisy-inputs/)
- Veo 3 (Google) is closed and claims SOTA on MovieGenBench and VBench (vendor blog claim). Sora 2 (OpenAI) is a proprietary text-to-video-plus-audio model that emphasises physical realism. Neither architecture was confirmed from primary sources. — [Novita AI blog](https://blogs.novita.ai/wan-2-2-vs-veo-3-which-is-the-better-match-for-you/); [Frameo](https://frameo.ai/blog/sora-veo-wan-feature-comparison/)
- Inference engineering for diffusion is a real cost lever. NVIDIA and Adobe report that FP8 on H100 cut latency by 60% and TCO by about 40% for a diffusion workload. — [Edge AI and Vision / NVIDIA](https://www.edge-ai-vision.com/2025/05/optimizing-transformer-based-diffusion-models-for-video-generation-with-nvidia-tensorrt/); [NVIDIA blog](https://developer.nvidia.com/blog/model-quantization-turn-fp8-checkpoints-into-high-performance-inference-engines-with-nvidia-tensorrt/)
- Video generators double as world models and synthetic data engines. Cosmos Transfer converts depth or lidar into photoreal video for robotics and AV training data. — [HF/NVIDIA](https://www.huggingface.co/blog/nvidia-physical-ai)

### Inferences
- Generative-vision skills are splitting into two tiers. (a) Using pretrained generators through APIs or ComfyUI is commoditised. (b) Training, fine-tuning (LoRA or control adapters), distilling (few-step samplers) and serving them efficiently is scarce and tied to inference cost.
- The convergence of video generation and world models for robotics and AV (Genie 3, Cosmos) means flow-matching expertise transfers into embodied AI and simulation. That makes it more durable than it would be as "media generation" alone.

### Gaps
- No job-posting data on generative-vision demand was found.
- Architecture claims for Veo 3 and Sora 2 are not verified.
- No data was found on the mix of image vs video generation work in industry.

---

## 5. Efficiency: edge and on-device inference, quantisation, TensorRT, NPUs, kernels

### Takeaway
Inference cost now drives a great deal of engineering. FP8 on NVIDIA GPUs gives measured wins of about 1.4x speed and about 48% smaller models for vision encoders. FP4 on edge hardware is still largely unproven, and FP8 can cost accuracy on edge detectors. GPU kernel and compiler engineers (CUDA, Triton, Pallas) command senior salaries of roughly $184k–$850k in postings, and recruiters describe them as the scarcest AI talent (opinion).

### Cited Findings
- FP8 TensorRT on CLIP (RTX 6000 Ada): the image encoder went from 588 MB to 306 MB (-48%) and from 166.2 ms to 119.8 ms (1.39x). The text encoder sped up 1.45x. — [NVIDIA Developer Blog](https://developer.nvidia.com/blog/model-quantization-turn-fp8-checkpoints-into-high-performance-inference-engines-with-nvidia-tensorrt/)
- A 2026 edge case study (Jetson-class) found that FP16 lost 0.2–0.4% accuracy vs FP32 while FP8 lost 3–5%, so FP16 was deployed. NVFP4 "could not be realised on either platform". Requesting the FP4 flag without explicit Q/DQ nodes *silently produces FP16 kernels*. — [arXiv 2608.14770](https://arxiv.org/pdf/2608.14770)
- NVIDIA claims NVFP4 uses about 3.5x less memory than FP16 and about 1.8x less than FP8. The examples are LLMs on DGX Station, and the guide recommends running your own evaluations. — [NVIDIA NVFP4 guide](https://build.nvidia.com/station/nvfp4-quantization)
- Edge toolchains are fragmented: TensorRT (NVIDIA), DRP-AI TVM (Renesas), SNPE (Qualcomm). — [TMA Solutions](https://www.tmasolutions.com/insights/ai-on-edge-device-revolutionizing-real-time-ai-with-nvidia-tensorrt-drp-ai-tvm-and-snpe)
- **Kernel-engineer demand, from postings:**
  - NVIDIA's Senior Performance Compiler Engineer (Triton) role requires 8+ years and pays $184k–$287.5k (posted 25 Feb 2026). — [AnitaB/NVIDIA](https://jobs.anitab.org/companies/nvidia/jobs/78098787-senior-performance-compiler-engineer-triton)
  - RadixArk wants 3+ years of production CUDA, Triton or Pallas kernels. — [Greenhouse](https://job-boards.greenhouse.io/radixark/jobs/4087888009)
  - DigitalOcean wants "expert-level proficiency in Triton or CUDA". — [Metaintro](https://www.metaintro.com/job/senior-engineer-2-at-digitalocean-d72eb3f8-1c6b-5179-8113-939bbd806ae9)
- Opinion (recruiter, HeroHunt 2026): GPU kernel engineers are "the scarcest talent in AI". There are millions of CUDA developers but "only a tiny elite" who can saturate a new chip. The guide cites an Anthropic GPU Performance Engineer role at $280k–$850k. — [HeroHunt](https://www.herohunt.ai/blog/how-to-recruit-gpu-kernel-engineers-2026/)

### Inferences
- Basic post-training quantisation (calling an INT8 or FP16 export) is commoditised by tooling. What is scarce is *verified* low-precision deployment: per-model accuracy evaluation, Q/DQ graph surgery, checking which kernels actually run (see the silent FP16 fallback), and calibration. The same goes for cross-NPU portability.
- Kernel and compiler skills are scarce mainly at the LLM and datacentre scale. For CV engineers, the most marketable version is "can profile and optimise a vision or VLA model end-to-end on Jetson, Qualcomm or Apple NPUs".

### Gaps
- No labour-market statistics (posting counts or growth) for kernel or edge roles; the evidence is postings plus a recruiter's opinion.
- No data on Apple ANE, Qualcomm Hexagon or MediaTek NPU adoption for vision.
- No INT4 vision-specific results.

---

## 6. Data-centric work: synthetic data, auto-labelling, evaluation, and AI coding assistants

### Takeaway
Foundation models (Grounding DINO, SAM 3, VLMs) now make first-pass labelling cheap, and world or video models (Cosmos Transfer) produce synthetic data. Auto-labels still fail on dense and fine-grained cases, so human review, data-engine design and evaluation design become the bottleneck. Expert opinion (Chip Huyen) puts evaluation at the centre of AI engineering. Karpathy (opinion) sees coding agents as useful but immature, which implies engineers shift toward specifying, reviewing and evaluating.

### Cited Findings
- Roboflow compared AI labels with human labels on 5 datasets. Auto-labels matched human quality on some but struggled on densely stocked retail coolers and multi-class trash. Roboflow's guidance is to keep humans for edge cases. — [Roboflow](https://blog.roboflow.com/ai-vs-human-labeled-data/)
- SAM 3's concept prompts ("find every X") directly target exhaustive instance labelling in images and video. — [Roboflow](https://blog.roboflow.com/what-is-sam3/)
- Synthetic data: Cosmos Transfer turns depth, segmentation or lidar into photoreal video for training. — [HF/NVIDIA](https://www.huggingface.co/blog/nvidia-physical-ai)
- Benchmark integrity is a live issue. The VGGT-Ω authors flag possible contamination in VGGT's released checkpoint, and Qwen3-VL's headline claims are self-reported. — [LearnOpenCV](https://learnopencv.com/vggt-vs-vggt-%cf%89-vggt-omega-a-complete-guide-to-feed-forward-3d-reconstruction/); [Simon Willison](https://simonwillison.net/2025/Sep/23/qwen3-vl)
- Opinion (Chip Huyen, *AI Engineering*, O'Reilly, Dec 2024 / Jan 2025): "the more AI is used... the more important evaluation becomes". The three focus areas of application development are evaluation, prompt engineering and AI interfaces. ML knowledge is "more of a nice-to-have" for AI engineering, but real-world problems "likely need both traditional ML engineering and AI engineering". — [Pragmatic Engineer excerpt](https://newsletter.pragmaticengineer.com/p/the-ai-engineering-stack); [ODSC summary](https://opendatascience.com/building-ai-applications-with-foundation-models-key-insights-from-chip-huyen/); [TWIML interview](https://twimlai.com/go/715)
- Opinion (Andrej Karpathy, Dwarkesh Patel podcast, Oct 2025): "it's the decade of agents", not the year of agents. He uses Claude Code and Codex but finds them immature: no continual learning, weak multimodality and reliability. While writing nanochat-style educational code, agents "kept writing it the ordinary way". He favours human–AI collaboration over fully autonomous coding. — [CO/AI summary](https://getcoai.com/news-letter/karpathy-says-ai-agents-are-a-decade-out/); [MIT Sloan ME](https://www.mitsloanme.com/?p=10868) (secondary sources; check against the episode)

### Inferences
- Labelling labour and boilerplate training code (data loaders, training loops, standard fine-tunes) are the most automated layers, through foundation-model auto-labelling and AI coding assistants. Designing the *data engine* is not automated: deciding what to label, active learning, finding failure slices, QA of auto-labels, and sim-to-real validation.
- Evaluation design is the common scarce skill across CV, VLM and robotics. This is reinforced by the trustworthiness problems of self-reported and contaminated benchmarks.

### Gaps
- No quantitative survey data was found on how AI coding assistants change ML engineers' time allocation.
- No 2025–2026 data on the size of the synthetic data market.
- Eugene Yan, Sebastian Raschka, Lilian Weng and a16z/Sequoia opinions were *not* retrieved in this session. Do not attribute positions to them without sourcing.

---

## 7. Commoditised vs durable vs scarce skills (synthesis)

### Takeaway
The evidence above supports a three-tier view. **Commoditised:** training standard CNN or ViT classifiers and detectors from scratch on curated data; basic fine-tuning or LoRA through high-level libraries; zero-shot VLM prompting; manual labelling; one-click quantisation and export. **Durable:** deep-learning fundamentals, multi-view geometry and probability, solid software engineering, experimental rigour. **Scarce and valuable:** performance and kernel engineering, verified low-precision and edge deployment, evaluation and benchmark design, data-engine and synthetic-data design, combining geometry with learning (3D, SLAM, feed-forward recon), robotics integration and VLA training, and serving and training large generative or world models.

### Cited Findings
- Frozen foundation backbones beat task-specific models on many dense tasks (Meta's claim), which erodes the bespoke-model moat. — [Meta AI](https://ai.meta.com/blog/dinov3-self-supervised-vision-model/)
- One-command "label with Grounding DINO, then train YOLO" pipelines exist (Autodistill), which commoditises the standard detector workflow. — [Roboflow](https://blog.roboflow.com/label-train-deploy-autodistill/)
- Auto-label failure on hard cases keeps humans and engineers in the loop. — [Roboflow](https://blog.roboflow.com/ai-vs-human-labeled-data/)
- Kernel and performance roles: senior, high pay, multiple employers; "scarcest talent" is the recruiter's opinion. — [HeroHunt](https://www.herohunt.ai/blog/how-to-recruit-gpu-kernel-engineers-2026/); [NVIDIA posting](https://jobs.anitab.org/companies/nvidia/jobs/78098787-senior-performance-compiler-engineer-triton)
- Quantisation pitfalls (silent FP16 fallback, 3–5% FP8 accuracy loss) show why verified deployment expertise matters. — [arXiv 2608.14770](https://arxiv.org/pdf/2608.14770)
- Evaluation is central (Chip Huyen, opinion). — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/the-ai-engineering-stack)
- Robotics and VLA labs hire for VLA plus imitation learning, and capital is heavy but concentrated. — [TechInterview PI guide](https://www.techinterview.org/post/3233477140/physical-intelligence-interview-guide/); [Dealroom](https://dealroom.co/charts/humanoid-robotics)
- Geometry combined with learning is at the research frontier (VGGT best paper; VGGT-Ω finalist) and splats are entering industry standards. — [CVF](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_VGGT_Visual_Geometry_Grounded_Transformer_CVPR_2025_paper.html); [Khronos](https://informedinfrastructure.com/post/khronos-announces-gltf-gaussian-splatting-extension)
- Coding agents are useful but immature (Karpathy, opinion), so engineering judgement and review remain human work for now. — [CO/AI](https://getcoai.com/news-letter/karpathy-says-ai-agents-are-a-decade-out/)

### Inferences
- **Commoditised or being automated (high confidence):**
  - training standard classifiers and detectors
  - dataset labelling
  - standard fine-tuning recipes
  - zero-shot VLM prompting
  - boilerplate PyTorch code (via AI coding assistants)
  - default ONNX/TensorRT export
- **Durable (high confidence):**
  - linear algebra, probability, optimisation
  - DL fundamentals: being able to read and implement papers
  - multi-view geometry and camera models
  - debugging and experimental design
  - production software engineering
- **Scarce (medium-to-high confidence):**
  1. Performance engineering: profiling, kernels in CUDA or Triton, compilers, and edge NPU deployment with accuracy verification.
  2. Evaluation design: in-domain test sets, failure slicing, guarding against contamination, LLM- or VLM-as-judge for vision tasks.
  3. Data engines: auto-label QA, active learning, synthetic data and sim-to-real.
  4. Combining 3D geometry with learning: splats, feed-forward reconstruction, SLAM fusion.
  5. Embodied AI: VLA training, teleop data pipelines, real-robot integration.
  6. Systems combined with ML: distributed training and serving of large VLMs, video and world models.
- Robotics and humanoid demand is the highest-growth but riskiest bet (capital-heavy, concentrated, China-weighted, deployment unproven). Efficiency and evaluation skills transfer across every sub-field and are the lowest-risk scarce bets.

### Gaps
- No direct labour-market data (e.g. Lightcast or LinkedIn) on CV skill demand trends was retrieved. The commoditised and scarce tiers are inferred from technology evidence plus postings.
- Expert opinions from Eugene Yan, Sebastian Raschka, Lilian Weng, a16z and Sequoia were not sourced here.
- No CVPR, ICCV or ECCV 2025 submission-trend statistics were retrieved.
