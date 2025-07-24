// NVIDIA GPU Financial Scoring Model Application

class GPUScoring {
    constructor() {
        // GPU data will be loaded from CSV
        this.gpuData = [];
        this.csvPath = 'scored.csv'; // Default path to the scored CSV file

        // Preset configurations
        this.presets = {
            balanced: { price_efficiency: 0.25, vram_capacity: 0.20, mig_capability: 0.15, power_efficiency: 0.15, form_factor: 0.10, connectivity: 0.15 },
            ai_training: { price_efficiency: 0.15, vram_capacity: 0.30, mig_capability: 0.25, power_efficiency: 0.10, form_factor: 0.05, connectivity: 0.15 },
            budget_conscious: { price_efficiency: 0.40, vram_capacity: 0.15, mig_capability: 0.10, power_efficiency: 0.20, form_factor: 0.10, connectivity: 0.05 },
            enterprise_efficiency: { price_efficiency: 0.20, vram_capacity: 0.20, mig_capability: 0.30, power_efficiency: 0.15, form_factor: 0.10, connectivity: 0.05 },
            compact_workstation: { price_efficiency: 0.20, vram_capacity: 0.15, mig_capability: 0.10, power_efficiency: 0.25, form_factor: 0.25, connectivity: 0.05 }
        };

        // Current weights
        this.weights = { ...this.presets.balanced };

        // Cached calculations
        this.normalizedData = {};
        this.scoredData = [];
        this.filteredData = [];

        // Chart instance
        this.scatterChart = null;

        // Initialize the application
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDataFromCSV().then(() => {
            this.normalizeData();
            this.calculateScores();
            this.updateDisplay();
            this.initializeChart();
        }).catch(error => {
            console.error("Error loading data:", error);
            // Fallback to sample data if available
            this.loadSampleData();
        });
    }

    async loadDataFromCSV() {
        try {
            const response = await fetch(this.csvPath);
            if (!response.ok) {
                throw new Error(`Failed to load CSV: ${response.status} ${response.statusText}`);
            }

            const csvText = await response.text();
            const rows = csvText.split('\n');
            const headers = rows[0].split(',');

            this.gpuData = [];

            for (let i = 1; i < rows.length; i++) {
                if (!rows[i].trim()) continue; // Skip empty rows

                const values = rows[i].split(',');
                const gpu = {};

                // Map CSV fields to our expected format
                for (let j = 0; j < headers.length; j++) {
                    const header = headers[j].trim();
                    const value = values[j] ? values[j].trim() : '';

                    // Convert values to appropriate types
                    if (header === 'canonical_model') {
                        gpu.Card_Name = value.replace(/_/g, ' '); // Replace underscores with spaces
                    } else if (header === 'price' || header === 'price_usd') {
                        gpu.Current_Retail_Price_USD = parseFloat(value) || 0;
                    } else if (header === 'vram_gb') {
                        gpu.VRAM_GB = parseInt(value) || 0;
                    } else if (header === 'mig_support') {
                        gpu.MIG_Support = parseInt(value) || 0;
                    } else if (header === 'tdp_watts') {
                        gpu.TDP_Watts = parseInt(value) || 0;
                    } else if (header === 'nvlink') {
                        gpu.NVLink_Support = value.toLowerCase() === 'true' ? 1 : 0;
                    } else if (header === 'score') {
                        // Store the original score, we'll scale it later
                        gpu.originalScore = parseFloat(value) || 0;
                    } else if (header === 'quantization_capable') {
                        gpu.quantization_capable = value.toLowerCase() === 'true';
                    } else if (header === 'generation') {
                        gpu.Generation = value;
                    } else if (header === 'slot_width') {
                        gpu.Slot_Width = parseInt(value) || 2; // Default to 2 if not specified
                    } else if (header === 'cuda_cores') {
                        gpu.CUDA_Cores = parseInt(value) || 0;
                    } else if (header === 'pcie_generation') {
                        gpu.PCIe_Generation = parseInt(value) || 4; // Default to 4 if not specified
                    }
                }

                // Set defaults for missing fields
                if (!gpu.Generation) {
                    // Try to infer generation from model name
                    if (gpu.Card_Name.includes('RTX 40') || gpu.Card_Name.includes('Ada')) {
                        gpu.Generation = 'Ada';
                    } else if (gpu.Card_Name.includes('RTX 30') || gpu.Card_Name.includes('A') || gpu.Card_Name.includes('Ampere')) {
                        gpu.Generation = 'Ampere';
                    } else if (gpu.Card_Name.includes('H100') || gpu.Card_Name.includes('Hopper')) {
                        gpu.Generation = 'Hopper';
                    } else if (gpu.Card_Name.includes('RTX 50') || gpu.Card_Name.includes('Blackwell')) {
                        gpu.Generation = 'Blackwell';
                    } else {
                        gpu.Generation = 'Unknown';
                    }
                }

                if (!gpu.CUDA_Cores) {
                    // Estimate CUDA cores based on model if not provided
                    if (gpu.Card_Name.includes('H100')) {
                        gpu.CUDA_Cores = 16896;
                    } else if (gpu.Card_Name.includes('A100')) {
                        gpu.CUDA_Cores = 6912;
                    } else if (gpu.Card_Name.includes('RTX 4090')) {
                        gpu.CUDA_Cores = 16384;
                    } else if (gpu.Card_Name.includes('RTX 3090')) {
                        gpu.CUDA_Cores = 10496;
                    } else {
                        gpu.CUDA_Cores = 5000; // Default value
                    }
                }

                if (!gpu.Slot_Width) {
                    gpu.Slot_Width = 2; // Default slot width
                }

                if (!gpu.PCIe_Generation) {
                    gpu.PCIe_Generation = 4; // Default PCIe generation
                }

                this.gpuData.push(gpu);
            }

            if (this.gpuData.length === 0) {
                throw new Error("No valid data found in CSV");
            }

            console.log(`Loaded ${this.gpuData.length} GPUs from CSV`);
        } catch (error) {
            console.error("Error loading CSV:", error);
            throw error;
        }
    }

    loadSampleData() {
        console.log("Loading sample data as fallback");
        // Sample data in case CSV loading fails
        this.gpuData = [
            {"Card_Name": "H100 PCIe 80GB", "Current_Retail_Price_USD": 30000, "VRAM_GB": 80, "MIG_Support": 7, "TDP_Watts": 350, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 16896, "Generation": "Hopper", "PCIe_Generation": 5, "quantization_capable": true},
            {"Card_Name": "A100 40GB", "Current_Retail_Price_USD": 10000, "VRAM_GB": 40, "MIG_Support": 7, "TDP_Watts": 250, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 6912, "Generation": "Ampere", "PCIe_Generation": 4, "quantization_capable": true},
            {"Card_Name": "RTX 4090", "Current_Retail_Price_USD": 1500, "VRAM_GB": 24, "MIG_Support": 0, "TDP_Watts": 450, "Slot_Width": 3, "NVLink_Support": 0, "CUDA_Cores": 16384, "Generation": "Ada", "PCIe_Generation": 4, "quantization_capable": false},
            {"Card_Name": "RTX 3090", "Current_Retail_Price_USD": 1000, "VRAM_GB": 24, "MIG_Support": 0, "TDP_Watts": 350, "Slot_Width": 3, "NVLink_Support": 0, "CUDA_Cores": 10496, "Generation": "Ampere", "PCIe_Generation": 4, "quantization_capable": false},
            {"Card_Name": "RTX A5000", "Current_Retail_Price_USD": 2500, "VRAM_GB": 24, "MIG_Support": 0, "TDP_Watts": 230, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 8192, "Generation": "Ampere", "PCIe_Generation": 4, "quantization_capable": true}
        ];

        this.normalizeData();
        this.calculateScores();
        this.updateDisplay();
        this.initializeChart();
    }

    setupEventListeners() {
        // Weight sliders
        const sliders = document.querySelectorAll('.weight-slider');
        sliders.forEach(slider => {
            slider.addEventListener('input', this.debounce(() => {
                this.updateWeights();
                this.calculateScores();
                this.updateDisplay();
            }, 100));
        });

        // Preset buttons
        const presetBtns = document.querySelectorAll('.preset-btn');
        presetBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const preset = e.target.dataset.preset;
                this.applyPreset(preset);
            });
        });

        // Reset button
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.applyPreset('balanced');
        });

        // Search input
        document.getElementById('searchInput').addEventListener('input', this.debounce(() => {
            this.filterData();
            this.updateTable();
        }, 300));

        // Table sorting
        const sortableHeaders = document.querySelectorAll('.sortable');
        sortableHeaders.forEach(header => {
            header.addEventListener('click', () => {
                this.sortTable(header.dataset.sort);
            });
        });

        // Export button
        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportToCSV();
        });

        // Chart tabs
        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchChartTab(e.target.dataset.tab);
            });
        });
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    normalizeData() {
        // Calculate min/max values for normalization
        const metrics = {
            price: { min: Math.min(...this.gpuData.map(gpu => gpu.Current_Retail_Price_USD)), max: Math.max(...this.gpuData.map(gpu => gpu.Current_Retail_Price_USD)) },
            vram: { min: Math.min(...this.gpuData.map(gpu => gpu.VRAM_GB)), max: Math.max(...this.gpuData.map(gpu => gpu.VRAM_GB)) },
            mig: { min: 0, max: 7 },
            tdp: { min: Math.min(...this.gpuData.map(gpu => gpu.TDP_Watts)), max: Math.max(...this.gpuData.map(gpu => gpu.TDP_Watts)) },
            slots: { min: 1, max: 3 },
            cuda: { min: Math.min(...this.gpuData.map(gpu => gpu.CUDA_Cores || 1000)), max: Math.max(...this.gpuData.map(gpu => gpu.CUDA_Cores || 20000)) },
            pcie: { min: 3, max: 5 }
        };

        this.normalizedData = this.gpuData.map(gpu => {
            // If we already have a score from the CSV, use it
            if (gpu.originalScore !== undefined) {
                return {
                    ...gpu,
                    scores: {
                        // Use the original score for all components if available
                        price_efficiency: gpu.originalScore,
                        vram_capacity: gpu.originalScore,
                        mig_capability: gpu.originalScore,
                        power_efficiency: gpu.originalScore,
                        form_factor: gpu.originalScore,
                        connectivity: gpu.originalScore
                    }
                };
            }

            // Otherwise calculate scores as before
            // Price efficiency (lower price per GB VRAM is better)
            const pricePerVRAM = gpu.Current_Retail_Price_USD / gpu.VRAM_GB;
            const minPricePerVRAM = Math.min(...this.gpuData.map(g => g.Current_Retail_Price_USD / g.VRAM_GB));
            const maxPricePerVRAM = Math.max(...this.gpuData.map(g => g.Current_Retail_Price_USD / g.VRAM_GB));
            const priceEfficiency = 1 - ((pricePerVRAM - minPricePerVRAM) / (maxPricePerVRAM - minPricePerVRAM));

            // VRAM capacity (higher is better)
            const vramScore = (gpu.VRAM_GB - metrics.vram.min) / (metrics.vram.max - metrics.vram.min);

            // MIG capability (higher is better)
            const migScore = gpu.MIG_Support / metrics.mig.max;

            // Power efficiency (lower TDP per CUDA core is better)
            const tdpPerCore = gpu.TDP_Watts / (gpu.CUDA_Cores || 5000); // Use default if CUDA_Cores is missing
            const minTdpPerCore = Math.min(...this.gpuData.map(g => g.TDP_Watts / (g.CUDA_Cores || 5000)));
            const maxTdpPerCore = Math.max(...this.gpuData.map(g => g.TDP_Watts / (g.CUDA_Cores || 5000)));
            const powerEfficiency = 1 - ((tdpPerCore - minTdpPerCore) / (maxTdpPerCore - minTdpPerCore));

            // Form factor (smaller slot width is better)
            const formFactor = 1 - ((gpu.Slot_Width - metrics.slots.min) / (metrics.slots.max - metrics.slots.min));

            // Connectivity (NVLink + PCIe generation)
            const connectivityScore = (gpu.NVLink_Support * 0.5) + (((gpu.PCIe_Generation || 4) - metrics.pcie.min) / (metrics.pcie.max - metrics.pcie.min) * 0.5);

            return {
                ...gpu,
                scores: {
                    price_efficiency: Math.max(0, Math.min(1, priceEfficiency)),
                    vram_capacity: vramScore,
                    mig_capability: migScore,
                    power_efficiency: Math.max(0, Math.min(1, powerEfficiency)),
                    form_factor: formFactor,
                    connectivity: connectivityScore
                }
            };
        });
    }

    calculateScores() {
        this.scoredData = this.normalizedData.map(gpu => {
            let compositeScore;

            // If we have an original score from the CSV, use it directly
            if (gpu.originalScore !== undefined) {
                compositeScore = gpu.originalScore;
            } else {
                // Otherwise calculate the composite score as before
                compositeScore = 
                    (gpu.scores.price_efficiency * this.weights.price_efficiency) +
                    (gpu.scores.vram_capacity * this.weights.vram_capacity) +
                    (gpu.scores.mig_capability * this.weights.mig_capability) +
                    (gpu.scores.power_efficiency * this.weights.power_efficiency) +
                    (gpu.scores.form_factor * this.weights.form_factor) +
                    (gpu.scores.connectivity * this.weights.connectivity);
            }

            return {
                ...gpu,
                compositeScore: compositeScore * 100 // Scale to 0-100
            };
        });

        // Sort by composite score
        this.scoredData.sort((a, b) => b.compositeScore - a.compositeScore);

        // Add rankings
        this.scoredData.forEach((gpu, index) => {
            gpu.rank = index + 1;
        });

        this.filterData();
    }

    filterData() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        this.filteredData = this.scoredData.filter(gpu => 
            gpu.Card_Name.toLowerCase().includes(searchTerm)
        );
    }

    updateWeights() {
        // Get current slider values
        const priceWeight = parseInt(document.getElementById('priceWeight').value);
        const vramWeight = parseInt(document.getElementById('vramWeight').value);
        const migWeight = parseInt(document.getElementById('migWeight').value);
        const powerWeight = parseInt(document.getElementById('powerWeight').value);
        const formWeight = parseInt(document.getElementById('formWeight').value);
        const connectWeight = parseInt(document.getElementById('connectWeight').value);

        // Calculate total
        const total = priceWeight + vramWeight + migWeight + powerWeight + formWeight + connectWeight;

        // Normalize to sum to 100% if needed
        if (total > 0) {
            this.weights = {
                price_efficiency: priceWeight / total,
                vram_capacity: vramWeight / total,
                mig_capability: migWeight / total,
                power_efficiency: powerWeight / total,
                form_factor: formWeight / total,
                connectivity: connectWeight / total
            };
        }

        // Update display values
        document.getElementById('priceWeightValue').textContent = `${Math.round(this.weights.price_efficiency * 100)}%`;
        document.getElementById('vramWeightValue').textContent = `${Math.round(this.weights.vram_capacity * 100)}%`;
        document.getElementById('migWeightValue').textContent = `${Math.round(this.weights.mig_capability * 100)}%`;
        document.getElementById('powerWeightValue').textContent = `${Math.round(this.weights.power_efficiency * 100)}%`;
        document.getElementById('formWeightValue').textContent = `${Math.round(this.weights.form_factor * 100)}%`;
        document.getElementById('connectWeightValue').textContent = `${Math.round(this.weights.connectivity * 100)}%`;
        document.getElementById('totalWeight').textContent = '100%';
    }

    applyPreset(presetName) {
        const preset = this.presets[presetName];
        if (!preset) return;

        this.weights = { ...preset };

        // Update sliders
        document.getElementById('priceWeight').value = Math.round(preset.price_efficiency * 100);
        document.getElementById('vramWeight').value = Math.round(preset.vram_capacity * 100);
        document.getElementById('migWeight').value = Math.round(preset.mig_capability * 100);
        document.getElementById('powerWeight').value = Math.round(preset.power_efficiency * 100);
        document.getElementById('formWeight').value = Math.round(preset.form_factor * 100);
        document.getElementById('connectWeight').value = Math.round(preset.connectivity * 100);

        // Update display
        this.updateWeights();
        this.calculateScores();
        this.updateDisplay();

        // Visual feedback
        const btn = document.querySelector(`[data-preset="${presetName}"]`);
        if (btn) {
            btn.classList.add('slide-in');
            setTimeout(() => btn.classList.remove('slide-in'), 400);
        }
    }

    updateDisplay() {
        this.updateTable();
        this.updateSummaryStats();
        this.updateScatterChart();
    }

    updateTable() {
        const tbody = document.getElementById('resultsBody');
        const displayData = this.filteredData.slice(0, 15); // Top 15

        tbody.innerHTML = displayData.map(gpu => {
            const rankClass = gpu.rank <= 3 ? `rank-${gpu.rank}` : '';
            const generationClass = `generation-${(gpu.Generation || 'unknown').toLowerCase()}`;
            const migClass = `mig-${gpu.MIG_Support === 0 ? '0' : gpu.MIG_Support >= 7 ? '7' : '4'}`;
            const quantClass = gpu.quantization_capable ? 'quant-capable' : 'quant-not-capable';

            return `
                <tr class="${rankClass} fade-in">
                    <td>${gpu.rank}</td>
                    <td class="gpu-name ${generationClass} ${quantClass}">${gpu.Card_Name}</td>
                    <td class="score-value">${gpu.compositeScore.toFixed(1)}</td>
                    <td class="price-value">${gpu.Current_Retail_Price_USD.toLocaleString()}</td>
                    <td class="vram-value">${gpu.VRAM_GB}</td>
                    <td><span class="mig-support ${migClass}">${gpu.MIG_Support || 'No'}</span></td>
                    <td class="tdp-value">${gpu.TDP_Watts}</td>
                    <td>${gpu.Slot_Width}</td>
                    <td>${gpu.quantization_capable ? '✓' : '✗'}</td>
                </tr>
            `;
        }).join('');
    }

    updateSummaryStats() {
        if (this.filteredData.length === 0) return;

        const avgScore = this.filteredData.reduce((sum, gpu) => sum + gpu.compositeScore, 0) / this.filteredData.length;
        const topPerformer = this.filteredData[0];
        const bestValue = this.filteredData.reduce((best, gpu) => 
            (gpu.Current_Retail_Price_USD / gpu.compositeScore) < (best.Current_Retail_Price_USD / best.compositeScore) ? gpu : best
        );
        const mostEfficient = this.filteredData.reduce((best, gpu) => 
            (gpu.TDP_Watts / gpu.CUDA_Cores) < (best.TDP_Watts / best.CUDA_Cores) ? gpu : best
        );

        document.getElementById('avgScore').textContent = avgScore.toFixed(1);
        document.getElementById('topPerformer').textContent = topPerformer.Card_Name;
        document.getElementById('bestValue').textContent = bestValue.Card_Name;
        document.getElementById('mostEfficient').textContent = mostEfficient.Card_Name;
    }

    sortTable(column) {
        // Remove existing sort classes
        document.querySelectorAll('.sortable').forEach(th => {
            th.classList.remove('asc', 'desc');
        });

        // Determine sort direction
        const currentHeader = document.querySelector(`[data-sort="${column}"]`);
        const isAsc = !currentHeader.classList.contains('asc');
        currentHeader.classList.add(isAsc ? 'asc' : 'desc');

        // Sort data
        this.filteredData.sort((a, b) => {
            let valueA, valueB;

            switch (column) {
                case 'rank':
                    valueA = a.rank;
                    valueB = b.rank;
                    break;
                case 'name':
                    valueA = a.Card_Name;
                    valueB = b.Card_Name;
                    break;
                case 'score':
                    valueA = a.compositeScore;
                    valueB = b.compositeScore;
                    break;
                case 'price':
                    valueA = a.Current_Retail_Price_USD;
                    valueB = b.Current_Retail_Price_USD;
                    break;
                case 'vram':
                    valueA = a.VRAM_GB;
                    valueB = b.VRAM_GB;
                    break;
                case 'mig':
                    valueA = a.MIG_Support;
                    valueB = b.MIG_Support;
                    break;
                case 'tdp':
                    valueA = a.TDP_Watts;
                    valueB = b.TDP_Watts;
                    break;
                case 'slots':
                    valueA = a.Slot_Width;
                    valueB = b.Slot_Width;
                    break;
                case 'quant':
                    // Sort by quantization capability (true values first)
                    valueA = a.quantization_capable === true ? 1 : 0;
                    valueB = b.quantization_capable === true ? 1 : 0;
                    break;
                default:
                    return 0;
            }

            if (typeof valueA === 'string') {
                return isAsc ? valueA.localeCompare(valueB) : valueB.localeCompare(valueA);
            }
            return isAsc ? valueA - valueB : valueB - valueA;
        });

        this.updateTable();
    }

    initializeChart() {
        const ctx = document.getElementById('scatterChart').getContext('2d');

        this.scatterChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'GPUs',
                    data: [],
                    backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Price vs Performance Score'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Price (USD)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Composite Score'
                        }
                    }
                }
            }
        });

        this.updateScatterChart();
    }

    updateScatterChart() {
        if (!this.scatterChart) return;

        // Group GPUs by quantization capability or generation
        const quantizationGroups = {
            true: [],
            false: []
        };

        const generationGroups = {};

        this.filteredData.slice(0, 20).forEach(gpu => {
            const dataPoint = {
                x: gpu.Current_Retail_Price_USD,
                y: gpu.compositeScore,
                gpu: gpu
            };

            // Group by quantization capability if available
            if (gpu.quantization_capable !== undefined) {
                quantizationGroups[gpu.quantization_capable].push(dataPoint);
            } 
            // Otherwise group by generation
            else if (gpu.Generation) {
                if (!generationGroups[gpu.Generation]) {
                    generationGroups[gpu.Generation] = [];
                }
                generationGroups[gpu.Generation].push(dataPoint);
            }
            // Fallback for GPUs with neither
            else {
                if (!generationGroups['Unknown']) {
                    generationGroups['Unknown'] = [];
                }
                generationGroups['Unknown'].push(dataPoint);
            }
        });

        // Determine which grouping to use
        let useQuantization = quantizationGroups[true].length > 0 || quantizationGroups[false].length > 0;

        // Create datasets based on grouping
        let datasets = [];

        if (useQuantization) {
            // Use quantization grouping
            datasets = [
                {
                    label: 'Quantization Capable',
                    data: quantizationGroups[true],
                    backgroundColor: '#4CAF50', // Green
                    pointRadius: 8,
                    pointHoverRadius: 10
                },
                {
                    label: 'Not Quantization Capable',
                    data: quantizationGroups[false],
                    backgroundColor: '#F44336', // Red
                    pointRadius: 8,
                    pointHoverRadius: 10
                }
            ];
        } else {
            // Use generation grouping
            const colors = {
                'Hopper': '#9C27B0', // Purple
                'Ada': '#2196F3',    // Blue
                'Ampere': '#FF9800', // Orange
                'Turing': '#795548', // Brown
                'Blackwell': '#009688', // Teal
                'Unknown': '#607D8B'  // Gray
            };

            datasets = Object.keys(generationGroups).map(generation => ({
                label: generation,
                data: generationGroups[generation],
                backgroundColor: colors[generation] || '#607D8B',
                pointRadius: 8,
                pointHoverRadius: 10
            }));
        }

        // Update chart with new datasets
        this.scatterChart.data.datasets = datasets;

        // Update chart options to show legend if we have multiple datasets
        this.scatterChart.options.plugins.legend.display = datasets.length > 1;

        // Add tooltips with GPU details
        this.scatterChart.options.plugins.tooltip = {
            callbacks: {
                label: function(context) {
                    const gpu = context.raw.gpu;
                    return [
                        `Model: ${gpu.Card_Name}`,
                        `Score: ${gpu.compositeScore.toFixed(1)}`,
                        `Price: $${gpu.Current_Retail_Price_USD.toLocaleString()}`,
                        `VRAM: ${gpu.VRAM_GB} GB`,
                        `MIG: ${gpu.MIG_Support || 'No'}`,
                        `TDP: ${gpu.TDP_Watts}W`,
                        gpu.quantization_capable !== undefined ? 
                            `Quantization: ${gpu.quantization_capable ? 'Yes' : 'No'}` : ''
                    ].filter(line => line !== '');
                }
            }
        };

        this.scatterChart.update();
    }

    switchChartTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update chart containers
        document.querySelectorAll('.chart-container').forEach(container => {
            container.classList.add('hidden');
        });

        const targetChart = document.getElementById(`chart${tabName === '2d' ? '2d' : tabName === '3d' ? '3d' : 'Scatter'}`);
        targetChart.classList.remove('hidden');

        // Update scatter chart if switching to it
        if (tabName === 'scatter') {
            setTimeout(() => {
                this.updateScatterChart();
            }, 100);
        }
    }

    exportToCSV() {
        const headers = ['Rank', 'GPU Name', 'Composite Score', 'Price (USD)', 'VRAM (GB)', 'MIG Support', 'TDP (W)', 'Slot Width'];
        const csvContent = [
            headers.join(','),
            ...this.filteredData.map(gpu => [
                gpu.rank,
                `"${gpu.Card_Name}"`,
                gpu.compositeScore.toFixed(1),
                gpu.Current_Retail_Price_USD,
                gpu.VRAM_GB,
                gpu.MIG_Support,
                gpu.TDP_Watts,
                gpu.Slot_Width
            ].join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'nvidia_gpu_scores.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GPUScoring();
});
