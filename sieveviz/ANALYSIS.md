Refined GPU Scoring and Rack Design for LLM Inference

Extended GPU Scoring Model for Heterogeneous Inference

To optimize for heterogeneous LLM inference workloads (simultaneously serving large 70B models and smaller 13B/7B models), we refine the GPU scoring logic to emphasize memory capacity and parallelism. In addition to the original metrics (price/perf, VRAM, power, etc.), we introduce new composite metrics that capture a GPU’s ability to handle both big models and many small models concurrently:
•	VRAM per Watt – GPU memory size relative to power draw (GB/W). Higher is better for memory-intensive models and energy efficiency.
•	MIG Instances per Slot – Maximum MIG (Multi-Instance GPU) slices per physical slot. This gauges how many isolated model instances a single card can run in parallel, normalized by form factor.
•	Cost per MIG Slice – Approximate cost per GPU partition, computed as price divided by MIG capacity (USD per slice). This helps identify cost-effective GPUs for multi-tenant inference.

We adjust the scoring weights to heavily favor VRAM capacity and MIG capability (for concurrency), while still considering price and power. For example, a heterogeneous inference preset might assign extra weight to memory and MIG (e.g. 25% VRAM, 20% MIG, 15% price, 15% power, 10% form factor, 15% connectivity). This ensures GPUs like the H100 80GB (large VRAM for big models) and L4 (efficient MIG slicing for many small models) rank higher than they would under a generic profile.

Normalization: Each metric is normalized 0–100 across the GPU dataset. For instance, VRAM per Watt is scaled such that the best GPU gets 100. In our data, the NVIDIA L4 (24 GB at 72 W) achieves ~0.333 GB/W – the highest memory-per-power ratio – thus near 100 points, whereas a 350 W card with 80 GB scores ~0.23 (around 69) ￼【18†】. Similarly, MIG per slot normalization gives 100 to GPUs that support 7 MIG instances in a single slot (like L40, L4, A2), and proportionally less to others.

After normalization, a weighted composite score is computed for each GPU. This composite reflects a GPU’s balanced ability to handle large-model shards (needs high VRAM and NVLink), and many small-model instances (needs many MIG slices and good efficiency).

Design Constraints: PCIe Form Factor and Power Limits

We constrain designs to PCIe-based GPUs (no SXM or HGX modules), using standard servers (4U chassis) with realistic power and cooling limits. A typical 4U server can host up to 8 double-slot GPUs (or more single-slot GPUs) and is generally limited to ~2.4 kW total draw for reliable operation (approximately 300 W per GPU slot, plus CPUs/overhead). Key constraints and considerations:
•	PCIe-Only Cards: All selected GPUs are PCIe add-in cards (including data center cards like H100 PCIe, A40, and pro visualization cards). We exclude SXM form factors that require special baseboards.
•	Slot Width: Many high-performance GPUs occupy 2 slots (or even 3 for certain consumer cards). Single-slot GPUs allow higher density per server. For example, an 8-GPU server can only fit 8 cards if they are 2-slot each (8×2 slots = 16 slots on a 4U board). But with single-slot cards, up to 16 might fit (if the motherboard supports enough slots and bandwidth).
•	Power per Server: We enforce ~2.4 kW/4U. In practice this means:
•	If using 300–350 W GPUs (e.g. A40 at 300 W, H100 PCIe at 350 W), limit to about 6–8 GPUs per 4U (8×350 W = 2.8 kW which is slightly over; 6×350 W = 2.1 kW, leaving room for CPU, fans, etc.).
•	Lower-power GPUs (70–150 W range) can fill all slots. For instance, 8×L4 (72 W each) is only ~576 W, well under budget – the limit here would be slot count or CPU PCIe lanes, not power.
•	Thermal/Cooling: Densely packing 8×300 W cards requires robust cooling (high CFM airflow or liquid). Single-slot cards at <75 W (which can often be passively cooled) are easier to cool in dense configurations, which favors designs like an L4-based server for dense inference.
•	Rack Unit Layout: We assume a standard 42U rack. A 4U server design means up to 10 such servers per rack (with 2U spare for top-of-rack switches or margin). We will present rack-level summaries assuming 42U racks for full deployment.

These constraints ensure that the proposed solutions are feasible in real-world data centers (power delivery, cooling, physical fit) and not just theoretically optimal on a per-card basis.

Multi-Metric Value Scores and Insights

By incorporating the new metrics, we gain insight into which GPUs are best suited for different aspects of inference:
•	VRAM per Watt: Highlights memory-efficient cards. The NVIDIA L4 tops this metric with ~0.333 GB/W (24 GB at 72 W)【18†】, making it excellent for memory-bound models at the edge. Other leaders include the RTX 4000 Ada SFF (~0.286 GB/W with 20 GB at 70 W) and A2 (0.267 GB/W with 16 GB at 60 W), as well as the upcoming Blackwell RTX 6000 (96 GB at 400 W = 0.24). In contrast, a 350 W flagship like H100 80GB provides ~0.229 GB/W – still good given its large memory, but the smaller cards deliver more VRAM per watt of power.
•	MIG Slices per Slot: Measures parallelism density. Several GPUs achieve the maximum 7 MIG instances per GPU (the hardware limit on A100/H100 class chips) and do so in a single-slot form factor, yielding 7 slices/slot. Notably, L40 (48 GB Ada), L4, and A2 can each be partitioned into 7 isolated GPU instances while occupying one slot【18†】. This is ideal for serving many small models concurrently. By comparison, a dual-slot card that supports 7 MIG instances (like A40 or H100 PCIe) achieves 3.5 slices per slot (7/2). GPUs with only 4 MIG instances (e.g. RTX 6000 Ada, Blackwell RTX 6000) in dual-slot form factor yield 2 slices/slot. The clear winners for MIG density are L4/A2/L40 for maximum instances per physical space.
•	Cost per MIG Slice: Favors cards that provide many partitions at lower cost. Using current retail prices, a RTX 4000 Ada SFF ($1250) with 4 MIG slices works out to **$312 per slice**, the cheapest in our list. Among 7-MIG cards, the A2 (~$2800) costs only $400 per slice, and L4 ($3500) about $500 per slice. These are much lower than, say, an H100 80GB ($30k, ~$4286 per slice)【18†】. This suggests that for sheer quantity of isolated instances (e.g. many small queries), clusters of mid-range GPUs can be far more cost-effective than a few ultra-high-end cards. Of course, each MIG slice on an A2/L4 has far less performance than a slice on H100 – but if the workload is dominated by many small models or low-throughput tasks, those cheaper slices might suffice.

We compile an extended GPU scorecard incorporating these new metrics, so decision-makers can sort and filter GPUs by the criteria that matter for their specific mix of models. An excerpt of this extended scorecard is shown below (CSV format):

Card_Name, VRAM_GB, TDP_W, Slot_Width, NVLink, MIG_Support, VRAM_per_Watt, MIG_per_Slot, Cost_per_MIG, Composite_Score
RTX L4,    24,      72,    1,         No,     7,           0.333,        7.0,         $500,        53.8
NVIDIA A2, 16,      60,    1,         No,     7,           0.267,        7.0,         $400,        43.4
RTX 6000 Ada, 48,   300,   2,         Yes,    4,           0.160,        2.0,         $1800,       50.8
H100 PCIe 80GB, 80, 350,   2,         No,     7,           0.229,        3.5,         $4286,       53.9
... (remaining GPUs) ...

(Table: Extended GPU scorecard snippet. “Composite_Score” here reflects a heterogeneous inference weighting. NVLink indicates presence of NVLink connectors for multi-GPU coupling. Cost_per_MIG is omitted for GPUs with no MIG capability.)

This data-driven scoring guides which GPUs to use in each scenario below.

NVLink, VRAM Pooling, and Model Sharding (vLLM)

Large models like a 70B parameter Transformer may exceed the memory of a single GPU, so we leverage multi-GPU sharding. Modern inference frameworks (e.g. vLLM) support tensor-parallel inference, splitting model layers across GPUs in one node ￼ ￼. To make this efficient, high-bandwidth interconnects between GPUs are crucial:
•	NVLink: Many pro/data-center GPUs can be connected via NVLink bridges, which provide direct GPU-to-GPU bandwidth up to 600 GB/s (bidirectional) ￼ – far higher than PCIe (PCIe 4.0 x16 ~32 GB/s each direction, PCIe 5.0 x16 ~64 GB/s each direction). NVLink allows faster weight and activation exchanges, effectively creating a larger pooled memory space across GPUs. For example, two 48 GB NVLink-connected cards can behave like a 96 GB memory pool for a model shard, with much lower latency than going through host memory.
•	PCIe Gen4/5: If NVLink is not available, PCIe can suffice for model parallelism up to a point ￼. PCIe 5.0 (as on H100 PCIe and upcoming Blackwell) at ~128 GB/s aggregate is sufficient for moderate multi-GPU inference, as demonstrated by recent experiments using two GPUs without NVLink ￼ ￼. However, for sustained high-throughput serving of one large model across many GPUs, NVLink or NVSwitch fabrics become important to avoid communication bottlenecks.
•	vLLM and Sharding: Frameworks like vLLM exploit these links by distributing weights evenly and keeping key-value caches across the GPUs. The benefit is twofold: larger models can be served (e.g. a 70B model split across 2×40 GB GPUs), and adding more GPUs can improve throughput by parallelizing computation ￼. The trade-off is some communication overhead and complexity of synchronization ￼. In our designs, we assume models like a 70B can be split across 2–4 GPUs within a single server. NVLink-connected pairs are used where possible for maximal bandwidth in multi-GPU “hot shards”.
•	MIG and NVLink Together: Note that MIG partitioning and NVLink are generally mutually exclusive modes on a given GPU – you either use the whole GPU (possibly NVLinked to another) for one big model, or split it into MIG slices for multiple models. However, a cluster can mix strategies at the rack level (some GPUs for MIG slices, others for NVLinked model shards). We incorporate this idea in the hybrid setup archetype below.

By integrating these assumptions, our rack designs can effectively serve a mix of model sizes: NVLink pairs or quads handle monolithic large-model inference with pooled memory, while MIG slices handle massively parallel small-model inference. Next, we present several rack-level archetypes optimized for different inference priorities. Each is described with a structured specification that could feed into tools like RackViz for visualization or be used to generate a Bill of Materials (BOM).

Rack Archetype Buildouts

Each archetype below is a reference design for a 42U rack (or portion of a rack) tailored to a specific inference scenario. We describe the GPU configuration and provide example JSON/YAML structures for integration with automation or visualization tools.

1. MIG-Slice Farm (High Parallelism per Rack)

Use-Case: Maximum concurrency for many small models (e.g. serving thousands of 7B parameter model instances). This design prioritizes MIG density and efficiency over individual GPU performance.
•	GPU Choice: NVIDIA L4 GPUs (Ada Lovelace, 24 GB, 72 W) – single-slot cards supporting 7 MIG partitions each ￼. L4 offers an excellent balance of memory (enough for 7B/13B models with 8-bit quantization), low power, and high MIG-per-dollar.
•	Server Configuration: 4U server with 10× L4 GPUs (taking advantage of single-slot form factor – 10 per 4U is feasible with riser cards). Each server provides up to 10×7 = 70 MIG instances. Total GPU power ~720 W (10×72 W), well under 2.4 kW including other components.
•	Rack: 10 such servers in a rack (40U for GPUs + 2U for networking/management). That yields 100 GPUs, 700 MIG slices in one rack. This could serve 700 independent model requests simultaneously (or fewer instances with more VRAM each, as MIG can be configured for different slice sizes).

Advantages: Exceptional throughput for many users/models, fine-grained allocation of GPU to tasks. Great for SaaS providers serving many lightweight AI models or microservices. Disadvantages: Not suited for very large models (>24 GB requirement each) – those cannot run on a single MIG slice here.

JSON configuration snippet:

{
"rack_archetype": "MIG-slice farm",
"servers_per_rack": 10,
"server_specs": {
"form_factor": "4U",
"GPUs": {
"model": "NVIDIA L4",
"count": 10,
"per_gpu": {
"VRAM_GB": 24,
"MIG_slices": 7,
"TDP_W": 72,
"NVLink": false,
"slot_width": 1
}
},
"total_GPU_power_W": 720,
"MIG_instances_per_server": 70
},
"total_MIG_instances_per_rack": 700,
"expected_power_per_server_W": 900,
"notes": "Optimized for maximum concurrent inference on 7B-13B models"
}

YAML configuration snippet:

rack_archetype: "MIG-slice farm"
servers_per_rack: 10
server_specs:
form_factor: 4U
GPUs:
model: NVIDIA L4
count: 10
per_gpu:
VRAM_GB: 24
MIG_slices: 7
TDP_W: 72
NVLink: false
slot_width: 1
total_GPU_power_W: 720
MIG_instances_per_server: 70
total_MIG_instances_per_rack: 700
expected_power_per_server_W: 900  # including CPU/overhead
notes: "Optimized for maximum concurrent inference on small models"

(The JSON/YAML above describe one server and the rack totals. They could be extended with per-rack totals or per-GPU details as needed by RackViz/BOM tools.)

2. 70B “Hot Shard” – Multi-GPU Big Model Server

Use-Case: Serving one instance of a very large model (e.g. a 70B param LLM) at high throughput (low latency, fully in GPU memory). This design uses few powerful GPUs with fast interconnect.
•	GPU Choice: NVIDIA RTX 6000 Ada (48 GB, NVLink) or the upcoming RTX 6000 Blackwell (96 GB, NVLink). These GPUs have high VRAM and NVLink support ￼ ￼. Two Blackwell 6000s NVLinked yield a 192 GB pool, enough for a 70B model in FP16 (or larger with compression). Alternatively, H100 80GB PCIe could be used, relying on PCIe 5.0 since NVLink is absent – in practice two H100 80GB with PCIe Gen5 can jointly serve a 70B model using tensor parallelism ￼ ￼.
•	Server Configuration: 4U server with 2–4 high-end GPUs. For example, 4× RTX 6000 Ada (dual-slot each) in one 4U. GPUs are paired via NVLink bridges (2+2) to effectively create two 96 GB nodes, or all-to-all if NVLink topology permits. In practice, one might use just 2 GPUs for a single 70B model shard to minimize communication overhead.
•	Rack: This is a specialized node; an entire rack could host multiple such “big model” servers if needed (each server handling a different model or used for load scaling). For instance, 10 servers each with 2× NVLinked 48 GB GPUs – each server holds one 70B model replica ready to serve queries with minimal latency (and one spare NVLink pair for redundancy or another model).

Advantages: Enables deployment of models that require >80 GB of memory, with maximal speed by keeping all weights in GPU memory and utilizing NVLink for fast GPU-GPU transfers ￼ ￼. Disadvantages: Very high cost per model instance; underutilized if the model is not fully saturated with work. Not flexible for smaller models (the big GPUs can be MIG-partitioned, but if they are busy with a large model, MIG isn’t used).

JSON example (for one server with 2 NVLinked GPUs):

{
"rack_archetype": "70B_hot_shard",
"servers_per_rack": 10,
"server_specs": {
"GPUs": [
{ "model": "RTX 6000 Ada", "VRAM_GB": 48, "NVLink": true },
{ "model": "RTX 6000 Ada", "VRAM_GB": 48, "NVLink": true }
],
"NVLink_pairs": [[0,1]],
"total_pooled_VRAM_GB": 96,
"tensor_parallel_size": 2,
"notes": "Each server: 2x 48GB GPUs NVLinked (96GB pooled) for one 70B model"
}
}

(This JSON indicates each server has 2 GPUs (index 0 and 1) bridged by NVLink into one pool. In a full rack, there would be 10 such servers each identical.)

3. Low-Watt Edge Inference Server

Use-Case: Edge deployment or micro-datacenter with limited power and cooling, still needing to run moderate AI inference. Target models are smaller (e.g. 7B or 13B with quantization) and request rates modest. Emphasis on energy efficiency and compact form factor.
•	GPU Choice: NVIDIA A2 (16 GB, 60 W) or T4 (16 GB, 70 W) GPUs. These are low-profile, single-slot cards optimized for inference at the edge. The A2 supports MIG (7 slices) ￼, which is unique for such a small card, allowing partitioning if needed.
•	Server Configuration: 1U or 2U short-depth server with 2–4 GPUs. For instance, a 1U box could host 2× A2 (since they are low-profile, no external power needed). A 2U could host 4× A2. Total GPU power in a 4×A2 system is only 240 W. These servers often have an efficient single-socket CPU and can run on 120 V AC if needed (max ~500 W draw).
•	Rack: In a telco or edge rack, you might fit 16 of these 2U servers (if 2U each, that’s 32U, plus network gear). That would be 64 A2 GPUs total in a rack, but only ~3.8 kW for the GPUs – well within typical edge rack power limits (often 5–8 kW).

Advantages: Very power-efficient (high inference per watt), minimal cooling requirements. Can be deployed in offices or edge sites with standard power circuits. Disadvantages: Limited performance per card – not suitable for heavy throughput or very large models. 16 GB VRAM per GPU means 13B is the upper limit (with quantization) for a single GPU; multi-GPU in such small servers is possible but those GPUs lack NVLink, so large models would be slow over PCIe.

YAML example (2U edge server with 4× A2):

rack_archetype: "low_watt_edge"
servers_per_rack: 16
server_specs:
form_factor: 2U short-depth
GPUs:
- model: NVIDIA A2
count: 4
per_gpu:
VRAM_GB: 16
TDP_W: 60
MIG_slices: 7
NVLink: false
total_GPU_power_W: 240
estimated_server_power_W: 400   # including CPU, etc.
notes: "Compact 2U edge server with 4x A2 (16GB) for low-power AI inferencing"

4. Budget Inference Density Rack

Use-Case: Maximize inference throughput per dollar invested. Ideal for organizations on a tight budget who still need significant GPU muscle, and are willing to manage higher power/cooling for cheaper cards. This design often leverages consumer or last-gen GPUs for best $/performance.
•	GPU Choice: NVIDIA RTX 4090 (24 GB, ~$1,600) or similar consumer GPUs offer very high raw performance per dollar ￼. The RTX 4090 (Ada) has 16,384 CUDA cores and excellent throughput for FP16/INT8, at a fraction of the cost of pro cards. Downside: 450 W TDP and 3-slot size, no NVLink, and only 24 GB VRAM (no MIG). Still, for many budget-conscious inference tasks (like running batches of medium-sized models or lots of smaller models via time-slicing), 4090s yield outstanding value.
•	Server Configuration: 4U air-cooled server with 4× RTX 4090. Given the 3-slot width of 4090s, at most 4 can physically fit (12 slots total out of 16, leaving some gaps for airflow). 4×450 W = 1800 W, which is within a 2.4 kW PSU budget (with a single CPU, etc., total ~2.1 kW). Each GPU is standalone (no NVLink) – they operate independently or via PCIe communication if needed.
•	Rack: 10 servers (4U each) would contain 40× RTX 4090 GPUs in one rack. That’s a massive 655,360 CUDA cores of total compute at roughly $66k in GPU cost – far cheaper per TFLOP than an equivalent number of A100/H100. However, power would be ~18 kW for GPUs alone, meaning this rack would require high-power circuits or run underclocked. More realistically, one might half-populate the rack (5 servers = 20 GPUs, ~9 kW) or use two racks for 10 servers.

Advantages: Unbeatable raw throughput per dollar. Great for batch inference or non-memory-intensive models that fit in 24 GB. Disadvantages: High power draw and heat density; not all data centers can accommodate 15–20 kW racks. Lacks enterprise features (ECC memory, NVLink, official support/warranty in servers). Also limited to models that fit on a single 24 GB card, since no NVLink to join memories (70B models are out of scope here, but 13B and smaller are fine).

JSON example (one budget server):

{
"rack_archetype": "budget_density",
"servers_per_rack": 5,
"server_specs": {
"form_factor": "4U",
"GPUs": {
"model": "GeForce RTX 4090",
"count": 4,
"per_gpu": {
"VRAM_GB": 24,
"TDP_W": 450,
"NVLink": false,
"MIG_slices": 0
}
},
"total_GPU_power_W": 1800
},
"notes": "4x RTX 4090 per server for max throughput per $. 5 servers (~9kW) shown; scale up if power allows."
}

5. NVLink-Enabled Hybrid Setup

Use-Case: A versatile deployment that can handle both large model inference (with multi-GPU pooling) and many simultaneous smaller models. This “hybrid” rack uses NVLink-capable GPUs that also support MIG, giving flexibility to reconfigure resources as needed.
•	GPU Choice: NVIDIA A100 40GB or A6000 48GB (Ampere generation) are good candidates – they have NVLink connectivity and sizable VRAM, but also can be partitioned (A100 supports MIG, A6000 does not officially support MIG but can time-slice). Another option is the upcoming Blackwell RTX 6000 (96GB) which supports 4 MIG instances and NVLink ￼ ￼. We will assume Blackwell 6000 for a forward-looking design: 96 GB VRAM each, NVLink bridges, and MIG (up to 4 slices).
•	Server Configuration: 4U server with 4× Blackwell RTX 6000 GPUs. Each is dual-slot 400 W. Four cards = 1600 W. NVLink bridges connect GPUs 1–2 and 3–4 (pairs) – so we have two pairs, each pair sharing 192 GB pooled memory. In MIG mode, each GPU could be split (e.g. 4×24 GB instances per GPU, yielding 16 slices per server). The system can thus be dynamically switched between two modes:
•	Mode A: Large-model mode – use NVLink pairs to host two different large models per server (each up to ~140B parameters if using 192 GB per model with memory optimization), or potentially gang all 4 GPUs for one model using both NVLink and PCIe (though without NVSwitch, cross-pair communication is slower).
•	Mode B: Multi-instance mode – configure MIG on all GPUs to get 16 isolated instances (with 24 GB each) per server, for serving many smaller models concurrently.
•	Rack: 10 servers (4U each) would provide 40 of these GPUs per rack. In Mode B that’s 160 MIG instances rack-wide. In Mode A, that’s up to 20 large-model deployments (2 per server). Realistically, a mix could be used: e.g. 5 servers in MIG mode, 5 in NVLink mode, or even some GPUs in each server allocated to each purpose – hence hybrid.

Advantages: Flexibility – can allocate resources to whatever workload is present (big model or many small models) by toggling MIG and grouping GPUs via NVLink. Offers a sort of “universal” inference cluster. Disadvantages: Complexity in management – one must reconfigure MIG mode and NVLink usage as workloads change ￼. Also, not as cost-efficient as specialized setups (these are expensive GPUs to also use for small tasks if those dominate).

YAML example (per server, hybrid config):

rack_archetype: "NVLink_hybrid"
server_specs:
form_factor: 4U
GPUs:
- model: RTX 6000 Blackwell
count: 4
per_gpu:
VRAM_GB: 96
TDP_W: 400
NVLink: true    # NVLink connectors present
MIG_slices: 4
NVLink_bridges:    # NVLink pairing configuration
- [0, 1]
- [2, 3]
modes:
large_model_mode:
GPUs_per_model: 2   # using NVLink pairs
pooled_VRAM_per_model_GB: 192
max_models_per_server: 2
mig_mode:
MIG_instances_per_gpu: 4
total_MIG_instances_per_server: 16
notes: >
4x 96GB GPUs per server. Can run in NVLink pairs for large models, or enable MIG for many smaller models.

This hybrid design could be a foundation for an inference service that needs to seamlessly scale between serving a few giant models (during certain tasks or off-peak times) and many smaller ones (during peak loads or multi-tenant scenarios) ￼ ￼. Administrators can dynamically re-provision the GPUs – for example, seven MIG instances during the day for many low-load tasks, then combining GPUs at night to speed up a big model job ￼.

⸻

Conclusion

In summary, we refined the GPU scoring to favor memory capacity, parallelism, and efficiency for mixed LLM inference workloads, and applied real-world constraints (PCIe form-factor, power, thermals) to our designs. We presented structured outputs – including an extended CSV scorecard and JSON/YAML configurations – for five rack-level archetypes:
•	MIG-Slice Farm: Maximizes concurrent inference instances using many low-power, MIG-capable GPUs.
•	70B Hot Shard: Uses a couple of high-memory GPUs (with NVLink) to serve one large model with low latency.
•	Low-Watt Edge Server: Provides AI inference at the edge with minimal power, using a few small GPUs in a compact server.
•	Budget Density Rack: Achieves highest throughput per dollar using consumer GPUs, trading off power and NVLink features.
•	NVLink-Enabled Hybrid: A versatile setup with high-end GPUs that can reconfigure between pooled-memory mode for big models and sliced mode for many models, as needed.

These designs can be directly fed into infrastructure planning tools. For example, the JSON/YAML can be imported into RackViz to generate a visual rack diagram, and the data can drive BOM generation (listing GPU models, counts, power supplies needed, etc.). By combining the structured metric-driven approach with clear physical constraints, these solutions help deploy inference hardware that is well-matched to the workload – whether that’s millions of lightweight chatbot instances or a handful of expert-level large language models.

Sources:
•	NVIDIA MIG allows up to 7 isolated GPU instances per physical GPU, enabling parallel inference on a single card ￼ ￼.
•	NVLink provides ~600 GB/s GPU-to-GPU bandwidth, vastly higher than PCIe (128 GB/s on PCIe 5.0), which is beneficial for multi-GPU model sharding ￼ ￼.
•	vLLM and similar frameworks support splitting large models across GPUs (tensor parallelism) to utilize combined memory and compute for faster inference ￼ ￼.
•	Data source: NVIDIA GPU specifications and pricing (Ada, Ampere, Hopper, Blackwell series) from provided dataset ￼ ￼, and scoring calculations (composite scores, VRAM/W, etc.) from analysis.