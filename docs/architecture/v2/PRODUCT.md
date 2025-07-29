# v2 Product Vision – Modular Infrastructure Signal Engine

## 🌐 Why We're Building This

The v2 evolution of the GPU Scoring Tool transforms it from a vertical pipeline into a **modular, category-agnostic
observability platform**. It exists to track and model the real-world behavior of computational hardware markets — not
just to scrape listings, but to extract meaning from infrastructure movement.

At its core, this is a system for answering questions like:

- What compute is actually undervalued right now?
- How do energy, memory, and quantization affect deployability?
- Where are supply cycles breaking down or dumping?
- What architectures are being phased out — and at what cost?

This system does not just provide pricing. It provides **insightful context**.

---

## 🧭 Product Utility

### For Operators

- Identifies arbitrage opportunities in GPU, DPU, and server listings
- Highlights underpriced cards for quantized model inference
- Tracks price decay of high-capex gear in liquidation cycles

### For Engineers

- Helps select optimal hardware for real-time AI deployment
- Surfaces MiG, VRAM, and thermal constraints for stacking
- Evaluates cards for quantized LLaMA/SDXL workloads

### For Analysts & Observers

- Maps resale and saturation cycles
- Tracks seller consolidation
- Enables speculative or forensic reasoning over compute markets

---

## 🪙 The Great Dumpening

We’re entering a cycle where:

- Enterprises offload hardware every 18–24 months
- AI hardware gets dumped before the software stack can catch up
- Inference-capable gear floods eBay, AliExpress, and OEM resellers
- DPUs, server racks, and SmartNICs follow a similar pattern

**The Great Dumpening** isn’t just about deals — it’s about pattern emergence.  
This project watches for those patterns.

---

## 🧩 Planned Signal Categories

Each of these will be implemented as a modular plugin under the v2 architecture:

### 1. GPUs (existing)

- Focus: Inference capacity, quantization compatibility, MiG, VRAM density
- Signals: $/GB, Models per Watt, $/MiG, 7B/13B/70B support

### 2. DPUs / SmartNICs (planned)

- Focus: Network-accelerated inference, NFV, offload capacity
- Signals: PCIe generation, RAM/logic, port density, firmware

### 3. x86 Servers (planned)

- Focus: Cold rack resale, blade systems, virtualization footprints
- Signals: Socket count, RAM ceiling, IOMMU/NVMe lanes, PSU redundancy

### 4. POWER9/POWER10 Systems (planned)

- Focus: Non-x86 inference stack viability, bandwidth-intensive compute
- Signals: PCIe bifurcation, OpenCAPI, NUMA performance, IBM DAX

### 5. AI Box Form Factors (R&D)

- Focus: Small footprint high-density platforms (Digits, DGX Station, Nvidia SOC)
- Signals: Co-located memory, NVLink topologies, DPU integration, system size

---

## 📈 Forecasting & Strategy

As the dataset matures, the product will:

- Enable delta-based forecasting over price drops
- Detect anomalous inventory shifts by vendor or SKU class
- Track repeated liquidation of same model (e.g., RTX A6000 vs PRO 6000 Blackwell)
- Feed into external pipelines for procurement automation or alerting

---

## 🔁 Data Loop

- Human-in-the-loop curated listings feed `glyphsieve`
- Plugins transform and score data per category
- `glyphd` exposes all signals over API
- Web UI reflects score deltas and multi-category breakdowns
- Reports and visualizations anchor time-series understanding

---

## 💡 Summary

The v2 product is a **live mirror of the compute gray market**.  
It watches where silicon goes after the hype fades.  
It spots undervalued capability before it’s scalped.  
And it helps operators think *three quarters ahead* — by listening to the whisper of inference in the wires.