
        let currentLang = 'zh';
        let quantumChartInstance = null;
        let blochScene, blochCamera, blochRenderer, blochVectorArrow, sphereMesh;
        let qubitState = { alpha: { re: 1, im: 0 }, beta: { re: 0, im: 0 } }; // Initial state |0>

        const CODE_PRESETS = {
            bell: `# 贝尔纠缠态 (Bell State |Φ+⟩ = (|00⟩ + |11⟩)/√2)\nimport quonic as q\n\nprog = q.QProgram(num_qubits=2)\nprog.h(0)          # 将 q0 置于叠加态\nprog.cnot(0, 1)    # 建立 q0 与 q1 的贝尔纠缠\nresult = prog.run(shots=1024)`,
            ghz: `# GHZ 3-量子比特极大纠缠态 (|000⟩ + |111⟩)/√2\nimport quonic as q\n\nprog = q.QProgram(num_qubits=3)\nprog.h(0)\nprog.cnot(0, 1)\nprog.cnot(1, 2)\nresult = prog.run(shots=1024)`,
            teleport: `# 量子隐形传态协议 (Quantum Teleportation)\nimport quonic as q\n\nprog = q.QProgram(num_qubits=3)\n# 1. 准备纠缠对 (q1, q2)\nprog.h(1)\nprog.cnot(1, 2)\n# 2. 状态传送 (q0 -> q2)\nprog.cnot(0, 1)\nprog.h(0)\nresult = prog.run(shots=1024)`,
            grover: `# Grover 搜索算法 (2-Qubit 演示 |11⟩)\nimport quonic as q\n\nprog = q.QProgram(num_qubits=2)\nprog.h(0)\nprog.h(1)\nprog.cz(0, 1)     # Oracle\nprog.h(0)\nprog.h(1)\nprog.x(0)\nprog.x(1)\nprog.cz(0, 1)\nprog.x(0)\nprog.x(1)\nprog.h(0)\nprog.h(1)\nresult = prog.run(shots=1024)`
        };

        function copyPipCommand() {
            const pipEl = document.getElementById('pip-command');
            if (!pipEl) return;
            const cmdText = pipEl.innerText;
            const tempTextArea = document.createElement('textarea');
            tempTextArea.value = cmdText;
            document.body.appendChild(tempTextArea);
            tempTextArea.select();
            document.execCommand('copy');
            document.body.removeChild(tempTextArea);

            const toast = document.getElementById('copy-toast');
            if (toast) {
                toast.style.opacity = '1';
                setTimeout(() => {
                    toast.style.opacity = '0';
                }, 2000);
            }
        }

        function toggleLanguage() {
            currentLang = currentLang === 'zh' ? 'en' : 'zh';
            const elements = document.querySelectorAll('[data-i18n-zh]');
            elements.forEach(el => {
                const text = el.getAttribute(`data-i18n-${currentLang}`);
                if (text) {
                    el.innerHTML = text;
                }
            });

            const presetSelect = document.getElementById('preset-select');
            if (presetSelect) {
                presetSelect.options[0].text = currentLang === 'zh' ? '贝尔纠缠态 (Bell State)' : 'Bell State |Φ+⟩';
                presetSelect.options[1].text = currentLang === 'zh' ? 'GHZ 3-量子比特态' : 'GHZ 3-Qubit State';
                presetSelect.options[2].text = currentLang === 'zh' ? '量子隐形传态 (Teleportation)' : 'Quantum Teleportation';
                presetSelect.options[3].text = currentLang === 'zh' ? 'Grover 搜索算法演示' : 'Grover Search Demo';
            }
        }

        function loadPresetCode() {
            const selectEl = document.getElementById('preset-select');
            const displayEl = document.getElementById('python-editor-display');
            if (selectEl && displayEl && CODE_PRESETS[selectEl.value]) {
                displayEl.textContent = CODE_PRESETS[selectEl.value];
            }
        }

        function runQuantumSimulation() {
            const selectEl = document.getElementById('preset-select');
            if (!selectEl) return;
            const presetKey = selectEl.value;

            let labels = [];
            let data = [];
            let wireHTML = '';
            let qubitCountStr = '2 Qubits';

            if (presetKey === 'bell') {
                qubitCountStr = '2 Qubits';
                labels = ['|00⟩', '|01⟩', '|10⟩', '|11⟩'];
                data = [516, 0, 0, 508];
                wireHTML = `
                    <div class="space-y-2 py-1 font-mono text-xs">
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_0:</span><span class="text-slate-500">─</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700"> H </span><span class="text-slate-500">───</span><span class="text-cyan-400 font-bold">●</span><span class="text-slate-500">───</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_1:</span><span class="text-slate-500">───────</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700">⊕</span><span class="text-slate-500">───</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                    </div>`;
            } else if (presetKey === 'ghz') {
                qubitCountStr = '3 Qubits';
                labels = ['|000⟩', '|001⟩', '|010⟩', '|011⟩', '|100⟩', '|101⟩', '|110⟩', '|111⟩'];
                data = [510, 0, 0, 0, 0, 0, 0, 514];
                wireHTML = `
                    <div class="space-y-2 py-1 font-mono text-xs">
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_0:</span><span class="text-slate-500">─</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700"> H </span><span class="text-slate-500">───</span><span class="text-cyan-400 font-bold">●</span><span class="text-slate-500">─────────</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_1:</span><span class="text-slate-500">───────</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700">⊕</span><span class="text-slate-500">───</span><span class="text-cyan-400 font-bold">●</span><span class="text-slate-500">───</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_2:</span><span class="text-slate-500">───────────</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700">⊕</span><span class="text-slate-500">───</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                    </div>`;
            } else if (presetKey === 'teleport') {
                qubitCountStr = '3 Qubits';
                labels = ['|000⟩', '|001⟩', '|010⟩', '|011⟩', '|100⟩', '|101⟩', '|110⟩', '|111⟩'];
                data = [252, 260, 255, 257, 0, 0, 0, 0];
                wireHTML = `
                    <div class="space-y-2 py-1 font-mono text-xs">
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_0:</span><span class="text-slate-500">───────────</span><span class="text-cyan-400 font-bold">●</span><span class="text-slate-500">───</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700"> H </span><span class="text-slate-500">───</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_1:</span><span class="text-slate-500">─</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700"> H </span><span class="text-slate-500">───</span><span class="text-cyan-400 font-bold">●</span><span class="text-slate-500">───</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700">⊕</span><span class="text-slate-500">───────</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_2:</span><span class="text-slate-500">───────</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700">⊕</span><span class="text-slate-500">───────────</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                    </div>`;
            } else if (presetKey === 'grover') {
                qubitCountStr = '2 Qubits';
                labels = ['|00⟩', '|01⟩', '|10⟩', '|11⟩'];
                data = [12, 10, 8, 994];
                wireHTML = `
                    <div class="space-y-2 py-1 font-mono text-xs">
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_0:</span><span class="text-slate-500">─</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700"> H </span><span class="text-slate-500">───</span><span class="text-cyan-400 font-bold">●</span><span class="text-slate-500">───</span><span class="bg-indigo-900/80 text-indigo-300 px-2 py-0.5 rounded border border-indigo-700"> Diff </span><span class="text-slate-500">───</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                        <div class="flex items-center space-x-2"><span class="text-cyan-400 font-bold w-8">q_1:</span><span class="text-slate-500">─</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700"> H </span><span class="text-slate-500">───</span><span class="bg-cyan-900/80 text-cyan-300 px-2 py-0.5 rounded border border-cyan-700">Z</span><span class="text-slate-500">───</span><span class="bg-indigo-900/80 text-indigo-300 px-2 py-0.5 rounded border border-indigo-700"> Diff </span><span class="text-slate-500">───</span><span class="bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">M</span></div>
                    </div>`;
            }

            const tagEl = document.getElementById('qubit-count-tag');
            const wireEl = document.getElementById('circuit-wire-container');
            if (tagEl) tagEl.innerText = qubitCountStr;
            if (wireEl) wireEl.innerHTML = wireHTML;

            const chartCanvas = document.getElementById('quantumChart');
            if (!chartCanvas) return;
            const ctx = chartCanvas.getContext('2d');
            if (quantumChartInstance) {
                quantumChartInstance.destroy();
            }

            quantumChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Shots Count (Total 1024)',
                        data: data,
                        backgroundColor: 'rgba(56, 189, 248, 0.7)',
                        borderColor: '#38bdf8',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const val = context.raw;
                                    const prob = ((val / 1024) * 100).toFixed(1);
                                    return ` Count: ${val} (${prob}%)`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1024,
                            grid: { color: 'rgba(255, 255, 255, 0.06)' },
                            ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#38bdf8', font: { family: 'JetBrains Mono', size: 12, weight: 'bold' } }
                        }
                    }
                }
            });
        }

        function initBlochSphere() {
            const container = document.getElementById('bloch-canvas-container');
            if (!container) return;

            const width = container.clientWidth || 380;
            const height = container.clientHeight || 380;

            blochScene = new THREE.Scene();

            blochCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
            blochCamera.position.set(2.6, 1.8, 3.2);
            blochCamera.lookAt(0, 0, 0);

            blochRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            blochRenderer.setSize(width, height);
            blochRenderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(blochRenderer.domElement);

            const sphereGeo = new THREE.SphereGeometry(1, 24, 18);
            const sphereMat = new THREE.MeshBasicMaterial({
                color: 0x38bdf8,
                wireframe: true,
                transparent: true,
                opacity: 0.15
            });
            sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
            blochScene.add(sphereMesh);

            const axesGroup = new THREE.Group();
            const createAxis = (from, to, colorHex) => {
                const mat = new THREE.LineBasicMaterial({ color: colorHex, linewidth: 2 });
                const geo = new THREE.BufferGeometry().setFromPoints([from, to]);
                return new THREE.Line(geo, mat);
            };
            axesGroup.add(createAxis(new THREE.Vector3(-1.2, 0, 0), new THREE.Vector3(1.2, 0, 0), 0xef4444));
            axesGroup.add(createAxis(new THREE.Vector3(0, -1.2, 0), new THREE.Vector3(0, 1.2, 0), 0x10b981));
            axesGroup.add(createAxis(new THREE.Vector3(0, 0, -1.2), new THREE.Vector3(0, 0, 1.2), 0x3b82f6));
            blochScene.add(axesGroup);

            const dir = new THREE.Vector3(0, 1, 0);
            blochVectorArrow = new THREE.ArrowHelper(dir, new THREE.Vector3(0, 0, 0), 1.0, 0xf43f5e, 0.2, 0.12);
            blochScene.add(blochVectorArrow);

            let isDragging = false;
            let prevMousePos = { x: 0, y: 0 };

            container.addEventListener('mousedown', (e) => {
                isDragging = true;
                prevMousePos = { x: e.clientX, y: e.clientY };
            });

            window.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                const deltaX = e.clientX - prevMousePos.x;
                const deltaY = e.clientY - prevMousePos.y;

                sphereMesh.rotation.y += deltaX * 0.01;
                axesGroup.rotation.y += deltaX * 0.01;
                blochVectorArrow.rotation.y += deltaX * 0.01;

                sphereMesh.rotation.x += deltaY * 0.01;
                axesGroup.rotation.x += deltaY * 0.01;
                blochVectorArrow.rotation.x += deltaY * 0.01;

                prevMousePos = { x: e.clientX, y: e.clientY };
            });

            window.addEventListener('mouseup', () => { isDragging = false; });

            function animate() {
                requestAnimationFrame(animate);
                blochRenderer.render(blochScene, blochCamera);
            }
            animate();

            window.addEventListener('resize', () => {
                if (!container) return;
                const w = container.clientWidth;
                const h = container.clientHeight;
                blochCamera.aspect = w / h;
                blochCamera.updateProjectionMatrix();
                blochRenderer.setSize(w, h);
            });
        }

        function applyBlochGate(gate) {
            let aR = qubitState.alpha.re, aI = qubitState.alpha.im;
            let bR = qubitState.beta.re, bI = qubitState.beta.im;

            if (gate === 'H') {
                const invSqrt2 = 1 / Math.sqrt(2);
                qubitState.alpha = { re: invSqrt2 * (aR + bR), im: invSqrt2 * (aI + bI) };
                qubitState.beta  = { re: invSqrt2 * (aR - bR), im: invSqrt2 * (aI - bI) };
            } else if (gate === 'X') {
                qubitState.alpha = { re: bR, im: bI };
                qubitState.beta  = { re: aR, im: aI };
            } else if (gate === 'Y') {
                qubitState.alpha = { re: bI, im: -bR };
                qubitState.beta  = { re: -aI, im: aR };
            } else if (gate === 'Z') {
                qubitState.beta = { re: -bR, im: -bI };
            } else if (gate === 'S') {
                qubitState.beta = { re: -bI, im: bR };
            } else if (gate === 'T') {
                const c = 1 / Math.sqrt(2);
                qubitState.beta = {
                    re: c * bR - c * bI,
                    im: c * bR + c * bI
                };
            }

            updateBlochVisuals();
        }

        function resetBlochState() {
            qubitState = { alpha: { re: 1, im: 0 }, beta: { re: 0, im: 0 } };
            updateBlochVisuals();
        }

        function updateBlochVisuals() {
            const aR = qubitState.alpha.re, aI = qubitState.alpha.im;
            const bR = qubitState.beta.re, bI = qubitState.beta.im;

            const x = 2 * (aR * bR + aI * bI);
            const y = 2 * (aR * bI - aI * bR);
            const z = (aR * aR + aI * aI) - (bR * bR + bI * bI);

            if (blochVectorArrow) {
                const dir = new THREE.Vector3(x, z, y).normalize();
                blochVectorArrow.setDirection(dir);
            }

            const theta = Math.acos(Math.min(Math.max(z, -1), 1));
            const phi = Math.atan2(y, x);

            const stateText = document.getElementById('bloch-state-text');
            const anglesText = document.getElementById('bloch-angles-text');
            const alphaStr = (aR >= 0 ? '+' : '') + aR.toFixed(3);
            const betaStr = (bR >= 0 ? '+' : '') + bR.toFixed(3);

            if (stateText) stateText.innerText = `|ψ⟩ = (${alphaStr}) |0⟩ + (${betaStr}) |1⟩`;
            if (anglesText) anglesText.innerText = `θ = ${theta.toFixed(2)} rad,  φ = ${(phi < 0 ? phi + 2 * Math.PI : phi).toFixed(2)} rad  [X:${x.toFixed(2)}, Y:${y.toFixed(2)}, Z:${z.toFixed(2)}]`;
        }

        function initQuantumBackground() {
            const canvas = document.getElementById('quantum-bg-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            let width = canvas.width = window.innerWidth;
            let height = canvas.height = window.innerHeight;

            const particles = [];
            const particleCount = Math.floor(Math.min(width, 1200) / 25);

            for (let i = 0; i < particleCount; i++) {
                particles.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    vx: (Math.random() - 0.5) * 0.4,
                    vy: (Math.random() - 0.5) * 0.4,
                    radius: Math.random() * 2 + 1,
                    color: Math.random() > 0.5 ? 'rgba(56, 189, 248, ' : 'rgba(129, 140, 248, '
                });
            }

            let scrollY = window.scrollY;
            window.addEventListener('scroll', () => {
                const diff = window.scrollY - scrollY;
                scrollY = window.scrollY;
                particles.forEach(p => {
                    p.y -= diff * 0.15;
                    if (p.y < 0) p.y = height;
                    if (p.y > height) p.y = 0;
                });

                if (sphereMesh) {
                    sphereMesh.rotation.y = window.scrollY * 0.001;
                    sphereMesh.rotation.z = Math.sin(window.scrollY * 0.001) * 0.1;
                }
            });

            window.addEventListener('resize', () => {
                width = canvas.width = window.innerWidth;
                height = canvas.height = window.innerHeight;
            });

            function renderParticles() {
                ctx.clearRect(0, 0, width, height);

                for (let i = 0; i < particles.length; i++) {
                    for (let j = i + 1; j < particles.length; j++) {
                        const dx = particles[i].x - particles[j].x;
                        const dy = particles[i].y - particles[j].y;
                        const dist = Math.sqrt(dx * dx + dy * dy);

                        if (dist < 120) {
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(56, 189, 248, ${0.12 * (1 - dist / 120)})`;
                            ctx.lineWidth = 0.8;
                            ctx.moveTo(particles[i].x, particles[i].y);
                            ctx.lineTo(particles[j].x, particles[j].y);
                            ctx.stroke();
                        }
                    }
                }

                particles.forEach(p => {
                    p.x += p.vx;
                    p.y += p.vy;

                    if (p.x < 0 || p.x > width) p.vx *= -1;
                    if (p.y < 0 || p.y > height) p.vy *= -1;

                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fillStyle = p.color + '0.6)';
                    ctx.fill();
                });

                requestAnimationFrame(renderParticles);
            }
            renderParticles();
        }

        function setupScrollObserver() {
            const revealElements = document.querySelectorAll('.reveal-on-scroll');

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');

                        if (entry.target.querySelector('#counter-expressiveness')) {
                            animateNumber('counter-expressiveness', 0, 100, 1200);
                        }
                    } else {
                        entry.target.classList.remove('is-visible');
                    }
                });
            }, { 
                threshold: 0.12,
                rootMargin: '0px 0px -30px 0px'
            });

            revealElements.forEach(el => observer.observe(el));
        }

        /* Documentation Modal Logic */
        function openDocsModal() {
            const modal = document.getElementById('docs-modal');
            if (modal) {
                modal.classList.remove('hidden');
                setTimeout(() => {
                    modal.classList.remove('opacity-0');
                }, 10);
            }
        }

        function closeDocsModal() {
            const modal = document.getElementById('docs-modal');
            if (modal) {
                modal.classList.add('opacity-0');
                setTimeout(() => {
                    modal.classList.add('hidden');
                }, 300);
            }
        }

        function switchDocTab(tabId) {
            const tabs = document.querySelectorAll('.doc-tab-content');
            tabs.forEach(tab => tab.classList.add('hidden'));

            const targetTab = document.getElementById(`doc-tab-${tabId}`);
            if (targetTab) {
                targetTab.classList.remove('hidden');
            }

            const btns = document.querySelectorAll('.doc-nav-btn');
            btns.forEach(btn => {
                if (btn.getAttribute('data-tab') === tabId) {
                    btn.classList.add('bg-slate-800', 'text-cyan-400');
                    btn.classList.remove('text-slate-300');
                } else {
                    btn.classList.remove('bg-slate-800', 'text-cyan-400');
                    btn.classList.add('text-slate-300');
                }
            });
        }

        function searchDocs() {
            const searchInput = document.getElementById('docs-search-input');
            if (!searchInput) return;
            const query = searchInput.value.toLowerCase();
            const tabs = document.querySelectorAll('.doc-tab-content');
            if (!query) {
                switchDocTab('overview');
                return;
            }
            tabs.forEach(tab => {
                const text = tab.innerText.toLowerCase();
                if (text.includes(query)) {
                    tab.classList.remove('hidden');
                } else {
                    tab.classList.add('hidden');
                }
            });
        }

        function animateNumber(id, start, end, duration) {
            const obj = document.getElementById(id);
            if (!obj || obj.getAttribute('data-animated')) return;
            obj.setAttribute('data-animated', 'true');

            let startTimestamp = null;
            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                obj.innerText = Math.floor(progress * (end - start) + start);
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                }
            };
            window.requestAnimationFrame(step);
        }

        window.onload = function() {
            const displayEl = document.getElementById('python-editor-display');
            if (displayEl) {
                displayEl.textContent = CODE_PRESETS.bell;
            }
            runQuantumSimulation();
            initBlochSphere();
            initQuantumBackground();
            setupScrollObserver();
        };
    