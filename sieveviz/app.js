// NVIDIA GPU Financial Scoring Model Application

class GPUScoring {
    constructor() {
        // GPU data from the provided dataset
        this.gpuData = [
            {"Card_Name": "RTX 6000 Ada", "Current_Retail_Price_USD": 7383.995, "VRAM_GB": 48, "MIG_Support": 4, "TDP_Watts": 300, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 18176, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "RTX 5000 Ada", "Current_Retail_Price_USD": 6650, "VRAM_GB": 32, "MIG_Support": 4, "TDP_Watts": 250, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 12800, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "RTX 4500 Ada", "Current_Retail_Price_USD": 2350, "VRAM_GB": 24, "MIG_Support": 4, "TDP_Watts": 210, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 7680, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "RTX 4000 Ada SFF", "Current_Retail_Price_USD": 1581.8, "VRAM_GB": 20, "MIG_Support": 4, "TDP_Watts": 70, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 6144, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "RTX A6000", "Current_Retail_Price_USD": 4439.0, "VRAM_GB": 48, "MIG_Support": 0, "TDP_Watts": 300, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 10752, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "RTX A5500", "Current_Retail_Price_USD": 2500, "VRAM_GB": 24, "MIG_Support": 0, "TDP_Watts": 230, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 7424, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "RTX A5000", "Current_Retail_Price_USD": 2400, "VRAM_GB": 24, "MIG_Support": 0, "TDP_Watts": 230, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 8192, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "RTX A4500", "Current_Retail_Price_USD": 1800, "VRAM_GB": 20, "MIG_Support": 0, "TDP_Watts": 200, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 7168, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "RTX A4000", "Current_Retail_Price_USD": 845.0, "VRAM_GB": 16, "MIG_Support": 0, "TDP_Watts": 140, "Slot_Width": 1, "NVLink_Support": 0, "CUDA_Cores": 6144, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "RTX A2000 12GB", "Current_Retail_Price_USD": 620, "VRAM_GB": 12, "MIG_Support": 0, "TDP_Watts": 70, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 3328, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "RTX A2000 6GB", "Current_Retail_Price_USD": 599.99, "VRAM_GB": 6, "MIG_Support": 0, "TDP_Watts": 70, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 3328, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "L40S", "Current_Retail_Price_USD": 15000, "VRAM_GB": 48, "MIG_Support": 7, "TDP_Watts": 350, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 18176, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "L40", "Current_Retail_Price_USD": 12000, "VRAM_GB": 48, "MIG_Support": 7, "TDP_Watts": 300, "Slot_Width": 1, "NVLink_Support": 0, "CUDA_Cores": 18176, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "A800 40GB", "Current_Retail_Price_USD": 15875.28, "VRAM_GB": 40, "MIG_Support": 7, "TDP_Watts": 300, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 10752, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "A40", "Current_Retail_Price_USD": 6300.0, "VRAM_GB": 48, "MIG_Support": 7, "TDP_Watts": 300, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 10752, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "H100 PCIe 80GB", "Current_Retail_Price_USD": 34995, "VRAM_GB": 80, "MIG_Support": 7, "TDP_Watts": 350, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 16896, "Generation": "Hopper", "PCIe_Generation": 5},
            {"Card_Name": "H800 PCIe 80GB", "Current_Retail_Price_USD": 30000, "VRAM_GB": 80, "MIG_Support": 7, "TDP_Watts": 350, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 14592, "Generation": "Hopper", "PCIe_Generation": 5},
            {"Card_Name": "L4", "Current_Retail_Price_USD": 2599.0, "VRAM_GB": 24, "MIG_Support": 7, "TDP_Watts": 72, "Slot_Width": 1, "NVLink_Support": 0, "CUDA_Cores": 7680, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "A2", "Current_Retail_Price_USD": 975.0, "VRAM_GB": 16, "MIG_Support": 7, "TDP_Watts": 60, "Slot_Width": 1, "NVLink_Support": 0, "CUDA_Cores": 3584, "Generation": "Ampere", "PCIe_Generation": 4},
            {"Card_Name": "RTX 4090", "Current_Retail_Price_USD": 1650, "VRAM_GB": 24, "MIG_Support": 0, "TDP_Watts": 450, "Slot_Width": 3, "NVLink_Support": 0, "CUDA_Cores": 16384, "Generation": "Ada", "PCIe_Generation": 4},
            {"Card_Name": "RTX 5090", "Current_Retail_Price_USD": 2000, "VRAM_GB": 32, "MIG_Support": 0, "TDP_Watts": 575, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 21760, "Generation": "Blackwell", "PCIe_Generation": 5},
            {"Card_Name": "RTX PRO 6000 Blackwell", "Current_Retail_Price_USD": 9299, "VRAM_GB": 96, "MIG_Support": 4, "TDP_Watts": 400, "Slot_Width": 2, "NVLink_Support": 1, "CUDA_Cores": 20480, "Generation": "Blackwell", "PCIe_Generation": 5},
            {"Card_Name": "RTX PRO 5000 Blackwell", "Current_Retail_Price_USD": 6000, "VRAM_GB": 48, "MIG_Support": 4, "TDP_Watts": 320, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 15360, "Generation": "Blackwell", "PCIe_Generation": 5},
            {"Card_Name": "RTX PRO 4500 Blackwell", "Current_Retail_Price_USD": 4000, "VRAM_GB": 32, "MIG_Support": 4, "TDP_Watts": 250, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 10240, "Generation": "Blackwell", "PCIe_Generation": 5},
            {"Card_Name": "RTX PRO 4000 Blackwell", "Current_Retail_Price_USD": 2500, "VRAM_GB": 24, "MIG_Support": 4, "TDP_Watts": 180, "Slot_Width": 2, "NVLink_Support": 0, "CUDA_Cores": 7680, "Generation": "Blackwell", "PCIe_Generation": 5}
        ];

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
            cuda: { min: Math.min(...this.gpuData.map(gpu => gpu.CUDA_Cores)), max: Math.max(...this.gpuData.map(gpu => gpu.CUDA_Cores)) },
            pcie: { min: 3, max: 5 }
        };

        this.normalizedData = this.gpuData.map(gpu => {
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
            const tdpPerCore = gpu.TDP_Watts / gpu.CUDA_Cores;
            const minTdpPerCore = Math.min(...this.gpuData.map(g => g.TDP_Watts / g.CUDA_Cores));
            const maxTdpPerCore = Math.max(...this.gpuData.map(g => g.TDP_Watts / g.CUDA_Cores));
            const powerEfficiency = 1 - ((tdpPerCore - minTdpPerCore) / (maxTdpPerCore - minTdpPerCore));

            // Form factor (smaller slot width is better)
            const formFactor = 1 - ((gpu.Slot_Width - metrics.slots.min) / (metrics.slots.max - metrics.slots.min));

            // Connectivity (NVLink + PCIe generation)
            const connectivityScore = (gpu.NVLink_Support * 0.5) + ((gpu.PCIe_Generation - metrics.pcie.min) / (metrics.pcie.max - metrics.pcie.min) * 0.5);

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
            const compositeScore = 
                (gpu.scores.price_efficiency * this.weights.price_efficiency) +
                (gpu.scores.vram_capacity * this.weights.vram_capacity) +
                (gpu.scores.mig_capability * this.weights.mig_capability) +
                (gpu.scores.power_efficiency * this.weights.power_efficiency) +
                (gpu.scores.form_factor * this.weights.form_factor) +
                (gpu.scores.connectivity * this.weights.connectivity);

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
            const generationClass = `generation-${gpu.Generation.toLowerCase()}`;
            const migClass = `mig-${gpu.MIG_Support === 0 ? '0' : gpu.MIG_Support >= 7 ? '7' : '4'}`;

            return `
                <tr class="${rankClass} fade-in">
                    <td>${gpu.rank}</td>
                    <td class="gpu-name ${generationClass}">${gpu.Card_Name}</td>
                    <td class="score-value">${gpu.compositeScore.toFixed(1)}</td>
                    <td class="price-value">${gpu.Current_Retail_Price_USD.toLocaleString()}</td>
                    <td class="vram-value">${gpu.VRAM_GB}</td>
                    <td><span class="mig-support ${migClass}">${gpu.MIG_Support || 'No'}</span></td>
                    <td class="tdp-value">${gpu.TDP_Watts}</td>
                    <td>${gpu.Slot_Width}</td>
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

        const chartData = this.filteredData.slice(0, 20).map(gpu => ({
            x: gpu.Current_Retail_Price_USD,
            y: gpu.compositeScore,
            gpu: gpu
        }));

        this.scatterChart.data.datasets[0].data = chartData;
        this.scatterChart.update('none');
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