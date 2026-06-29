const { useState, useEffect, useRef } = React;

function App() {
    const [stats, setStats] = useState({ total_good: 0, total_bad: 0 });
    const [settings, setSettings] = useState({ model_path: 'yolov8n.pt', belt_speed_delay: 2.5, threshold_bad_area: 10.0, counting_line_y: 80.0, counting_orientation: 'horizontal' });
    const [modelClasses, setModelClasses] = useState([]);
    const [availableModels, setAvailableModels] = useState([]);
    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef(null);
    const [frameBase64, setFrameBase64] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [activeModel, setActiveModel] = useState("Lade...");
    const [performance, setPerformance] = useState({ fps: 0, inf_time: 0 });

    useEffect(() => {
        // Fetch Settings
        fetch('/api/settings')
            .then(res => res.json())
            .then(data => setSettings(data))
            .catch(err => console.error("Could not load settings:", err));

        // Fetch Models
        fetchModels();

        // Connect Websocket
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${wsProtocol}//${window.location.host}/ws/video`);

        ws.onopen = () => setIsConnected(true);
        ws.onclose = () => setIsConnected(false);
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.frame) {
                setFrameBase64(`data:image/jpeg;base64,${data.frame}`);
            }
            if (data.stats) {
                setStats(data.stats);
            }
            if (data.active_model) {
                setActiveModel(data.active_model);
            }
            if (data.fps !== undefined) {
                setPerformance({ fps: data.fps, inf_time: data.inf_time });
            }
        };

        return () => ws.close();
    }, []);

    useEffect(() => {
        let isActive = true;
        if (settings.model_path) {
            fetch(`/api/models/${settings.model_path}/classes`)
                .then(res => res.json())
                .then(data => {
                    if (isActive && data.classes) setModelClasses(data.classes);
                })
                .catch(err => console.error("Could not load classes:", err));
        }
        return () => { isActive = false; };
    }, [settings.model_path]);

    const fetchModels = () => {
        fetch('/api/models')
            .then(res => res.json())
            .then(data => setAvailableModels(data.models))
            .catch(err => console.error("Could not load models:", err));
    };

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('/api/models/upload', {
                method: 'POST',
                body: formData
            });
            if (res.ok) {
                alert('Modell erfolgreich hochgeladen!');
                fetchModels();
                handleSettingChange('model_path', file.name);
            } else {
                alert('Fehler beim Upload (Nur .pt oder .engine erlaubt).');
            }
        } catch (err) {
            alert('Upload fehlgeschlagen!');
        }
        setUploading(false);
        if (fileInputRef.current) fileInputRef.current.value = '';
    };

    const saveSettings = async () => {
        try {
            await fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });

            const mapping = {};
            modelClasses.forEach(cls => {
                mapping[cls.id] = {
                    action: cls.action,
                    confidence: cls.confidence !== undefined ? cls.confidence : 0.5
                };
            });

            await fetch(`/api/models/${settings.model_path}/mapping`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(mapping)
            });

            alert('Einstellungen gespeichert!');
        } catch (err) {
            alert('Fehler beim Speichern der Einstellungen');
        }
    };

    const handleClassActionChange = (classId, newAction) => {
        setModelClasses(prev => prev.map(cls => cls.id === classId ? { ...cls, action: newAction } : cls));
    };

    const handleClassConfidenceChange = (classId, newConfidence) => {
        setModelClasses(prev => prev.map(cls => cls.id === classId ? { ...cls, confidence: newConfidence } : cls));
    };

    const handleSettingChange = (key, val) => {
        setSettings(prev => ({ ...prev, [key]: val }));
    };

    return (
        <div className="flex flex-col h-full w-full bg-gradient-to-br from-gray-100 to-gray-200">
            {/* Header */}
            <header className="glass px-6 py-4 flex justify-between items-center shadow-sm z-10">
                <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]' : 'bg-red-500'}`}></div>
                    <h1 className="text-2xl font-bold text-gray-800 tracking-tight">Potato Sorter</h1>
                    <div className="ml-4 px-3 py-1 bg-white/60 rounded-lg border border-gray-200 text-xs font-mono text-gray-600 hidden sm:block">
                        Model: <span className="font-semibold text-indigo-600">{activeModel}</span>
                    </div>
                    <div className="ml-2 flex items-center gap-3 px-3 py-1 bg-white/60 rounded-lg border border-gray-200 text-xs font-mono text-gray-600 hidden md:flex">
                        <span>FPS: <span className="font-semibold text-indigo-600">{performance.fps.toFixed(1)}</span></span>
                        <span className="text-gray-300">|</span>
                        <span>Infer.: <span className="font-semibold text-indigo-600">{performance.inf_time.toFixed(1)} ms</span></span>
                    </div>
                </div>
                <div className="flex gap-4">
                    <button
                        onClick={() => setActiveTab('dashboard')}
                        className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === 'dashboard' ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-600 hover:bg-white/50'}`}>
                        Dashboard
                    </button>
                    <button
                        onClick={() => setActiveTab('settings')}
                        className={`px-4 py-2 rounded-lg font-medium transition-colors ${activeTab === 'settings' ? 'bg-indigo-600 text-white shadow-md' : 'text-gray-600 hover:bg-white/50'}`}>
                        Einstellungen
                    </button>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 p-6 overflow-auto">
                {activeTab === 'dashboard' ? (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
                        {/* Video Feed */}
                        <div className="lg:col-span-2 glass rounded-2xl overflow-hidden shadow-lg flex flex-col">
                            <div className="px-4 py-3 border-b border-white/40 bg-white/30 backdrop-blur-md">
                                <h2 className="font-semibold text-gray-700">Live Kamera</h2>
                            </div>
                            <div className="flex-1 bg-black relative flex items-center justify-center">
                                {frameBase64 ? (
                                    <img src={frameBase64} alt="Live Feed" className="max-h-full max-w-full object-contain" />
                                ) : (
                                    <div className="text-gray-400 flex flex-col items-center animate-pulse-slow">
                                        <svg className="w-12 h-12 mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                                        <span>Warte auf Kamerabild...</span>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Stats Panel */}
                        <div className="flex flex-col gap-4">
                            <div className="glass rounded-2xl p-5 shadow-lg flex-1 flex flex-col justify-center items-center transform transition-transform hover:scale-[1.02]">
                                <div className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Gute Kartoffeln</div>
                                <div className="text-5xl font-black text-green-600">{stats.total_good}</div>
                            </div>
                            <div className="glass rounded-2xl p-5 shadow-lg flex-1 flex flex-col justify-center items-center transform transition-transform hover:scale-[1.02]">
                                <div className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Ausschuss (Schlecht)</div>
                                <div className="text-5xl font-black text-red-500">{stats.total_bad}</div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="max-w-3xl mx-auto glass rounded-3xl shadow-xl overflow-hidden mt-8">
                        <div className="px-8 py-6 bg-white/40 border-b border-white/40">
                            <h2 className="text-2xl font-bold text-gray-800">Systemeinstellungen</h2>
                        </div>
                        <div className="p-8 space-y-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">YOLO Modell (.pt oder .engine)</label>
                                <div className="flex gap-3">
                                    <select
                                        value={settings.model_path}
                                        onChange={(e) => handleSettingChange('model_path', e.target.value)}
                                        className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none bg-white"
                                    >
                                        {availableModels.map(m => (
                                            <option key={m} value={m}>{m}</option>
                                        ))}
                                    </select>
                                    <button
                                        onClick={() => fileInputRef.current.click()}
                                        disabled={uploading}
                                        className="px-4 py-3 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 font-medium rounded-xl transition-all flex items-center gap-2 whitespace-nowrap">
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                                        {uploading ? 'Lädt...' : 'Modell Hochladen'}
                                    </button>
                                    <input
                                        type="file"
                                        ref={fileInputRef}
                                        onChange={handleUpload}
                                        accept=".pt,.engine"
                                        className="hidden"
                                    />
                                </div>
                            </div>

                            {modelClasses.length > 0 && (
                                <div className="bg-white/50 rounded-xl p-4 border border-gray-100">
                                    <h3 className="text-sm font-semibold text-gray-700 mb-3">Klassen-Zuweisung für {settings.model_path}</h3>
                                    <div className="space-y-3">
                                        {modelClasses.map(cls => (
                                            <div key={cls.id} className="flex flex-col bg-white px-4 py-3 rounded-lg border border-gray-100 shadow-sm gap-2">
                                                <div className="flex items-center justify-between">
                                                    <span className="font-mono text-sm font-medium text-gray-800">#{cls.id} - {cls.name}</span>
                                                    <select
                                                        value={cls.action}
                                                        onChange={(e) => handleClassActionChange(cls.id, e.target.value)}
                                                        className="px-3 py-1.5 rounded-lg border border-gray-200 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                                                    >
                                                        <option value="ignore">Ignorieren</option>
                                                        <option value="good">Gut (Behalten)</option>
                                                        <option value="bad">Schlecht (Aussortieren)</option>
                                                    </select>
                                                </div>
                                                <div className="flex items-center justify-between mt-1">
                                                    <span className="text-xs text-gray-500 font-medium">Sicherheit: {Math.round((cls.confidence !== undefined ? cls.confidence : 0.5) * 100)}%</span>
                                                    <input
                                                        type="range"
                                                        min="0.05" max="0.95" step="0.05"
                                                        value={cls.confidence !== undefined ? cls.confidence : 0.5}
                                                        onChange={(e) => handleClassConfidenceChange(cls.id, parseFloat(e.target.value))}
                                                        className="w-1/2 h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                                    />
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Förderband-Verzögerung bis Auswurf (Sekunden): <span className="font-bold text-indigo-600">{settings.belt_speed_delay}s</span></label>
                                <input
                                    type="range"
                                    min="0.5" max="10" step="0.1"
                                    value={settings.belt_speed_delay}
                                    onChange={(e) => handleSettingChange('belt_speed_delay', parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                />
                                <div className="flex justify-between text-xs text-gray-400 mt-2">
                                    <span>0.5s</span>
                                    <span>10.0s</span>
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Ausrichtung der Zähllinie</label>
                                    <select
                                        value={settings.counting_orientation || 'horizontal'}
                                        onChange={(e) => handleSettingChange('counting_orientation', e.target.value)}
                                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none bg-white"
                                    >
                                        <option value="horizontal">Horizontal (Oben nach Unten)</option>
                                        <option value="vertical">Vertikal (Links nach Rechts)</option>
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">Zähllinie Position in %: <span className="font-bold text-indigo-600">{settings.counting_line_y || 80}%</span></label>
                                    <input
                                        type="range"
                                        min="10" max="100" step="1"
                                        value={settings.counting_line_y || 80}
                                        onChange={(e) => handleSettingChange('counting_line_y', parseFloat(e.target.value))}
                                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600 mt-3"
                                    />
                                    <div className="flex justify-between text-xs text-gray-400 mt-2">
                                        <span>{settings.counting_orientation === 'vertical' ? 'Links (10%)' : 'Oben (10%)'}</span>
                                        <span>{settings.counting_orientation === 'vertical' ? 'Rechts (100%)' : 'Unten (100%)'}</span>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Toleranz: Schlechte Fläche (%): <span className="font-bold text-indigo-600">{settings.threshold_bad_area}%</span></label>
                                <input
                                    type="range"
                                    min="0" max="50" step="1"
                                    value={settings.threshold_bad_area}
                                    onChange={(e) => handleSettingChange('threshold_bad_area', parseFloat(e.target.value))}
                                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                                />
                            </div>
                        </div>
                        <div className="px-8 py-5 bg-gray-50/50 border-t border-gray-100 flex justify-end">
                            <button
                                onClick={saveSettings}
                                className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl shadow-lg shadow-indigo-200 transition-all active:scale-95">
                                Einstellungen Speichern
                            </button>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
