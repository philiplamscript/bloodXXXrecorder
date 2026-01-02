import React, { useState, useMemo, useRef, useEffect } from 'react';
import { 
  Users, 
  Vote, 
  ShieldAlert, 
  FileText, 
  RotateCcw, 
  Plus, 
  Trash2, 
  Calendar,
  Zap,
  Skull, 
  Filter,
  X,
  ChevronUp,
  ChevronDown,
  ArrowUpDown,
  RefreshCcw,
  AlertTriangle
} from 'lucide-react';

// Types
interface Player {
  no: number;
  inf: string;
  day: string; 
  reason: string; 
  red: string;
}

interface Nomination {
  id: string;
  day: number;
  way: string;
  voters: string; 
  note: string;
}

interface Character {
  name: string;
  status: '0' | '1' | '2';
  note: string;
}

interface CharDict {
  Outsider: Character[];
  Minion: Character[];
  Demon: Character[];
}

interface SortConfig {
  key: keyof Player | null;
  direction: 'asc' | 'desc';
}

const INITIAL_PLAYERS = 18;

const createInitialChars = (): CharDict => ({
  Outsider: Array(8).fill(null).map(() => ({ name: '', status: '0', note: '' })),
  Minion: Array(8).fill(null).map(() => ({ name: '', status: '0', note: '' })),
  Demon: Array(8).fill(null).map(() => ({ name: '', status: '0', note: '' })),
});

export default function App() {
  const [activeTab, setActiveTab] = useState<'players' | 'votes' | 'chars' | 'notes'>('players');
  const [players, setPlayers] = useState<Player[]>(
    Array.from({ length: INITIAL_PLAYERS }, (_, i) => ({
      no: i + 1,
      inf: '', day: '', reason: '', red: '',
    }))
  );
  const [nominations, setNominations] = useState<Nomination[]>([
    { id: '1', day: 1, way: '', voters: '', note: '' }
  ]);
  const [chars, setChars] = useState<CharDict>(createInitialChars());
  const [note, setNote] = useState('');
  
  const [showResetConfirm, setShowResetConfirm] = useState(false);
  const [selectedInFilter, setSelectedInFilter] = useState<number[]>([]);
  const [activeFilter, setActiveFilter] = useState<number[]>([]);
  const [sortConfig, setSortConfig] = useState<SortConfig>({ key: null, direction: 'asc' });

  const notesTextareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (activeTab === 'notes' && notesTextareaRef.current) {
      notesTextareaRef.current.style.height = 'auto';
      notesTextareaRef.current.style.height = `${notesTextareaRef.current.scrollHeight}px`;
    }
  }, [note, activeTab]);

  const handleSoftReset = () => {
    setPlayers(prev => prev.map(p => ({ ...p, inf: '', day: '', reason: '', red: '' })));
    setNominations([{ id: Math.random().toString(36).substr(2, 9), day: 1, way: '', voters: '', note: '' }]);
    setChars(prev => {
      const newChars = { ...prev };
      (Object.keys(newChars) as Array<keyof CharDict>).forEach(faction => {
        newChars[faction] = newChars[faction].map(c => ({
          ...c,
          status: '0',
          note: ''
        }));
      });
      return newChars;
    });
    setNote('');
    setActiveFilter([]);
    setSelectedInFilter([]);
    setShowResetConfirm(false);
  };

  const sortedPlayers = useMemo(() => {
    let sortablePlayers = [...players];
    if (sortConfig.key !== null) {
      sortablePlayers.sort((a, b) => {
        const aValue = a[sortConfig.key!];
        const bValue = b[sortConfig.key!];
        if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }
    return sortablePlayers;
  }, [players, sortConfig]);

  const requestSort = (key: keyof Player) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIcon = (key: keyof Player) => {
    if (sortConfig.key !== key) return <ArrowUpDown size={8} className="opacity-30" />;
    return sortConfig.direction === 'asc' ? <ChevronUp size={8} /> : <ChevronDown size={8} />;
  };

  const visiblePlayerNumbers = useMemo(() => {
    const all = Array.from({ length: INITIAL_PLAYERS }, (_, i) => i + 1);
    return activeFilter.length > 0 ? all.filter(num => activeFilter.includes(num)) : all;
  }, [activeFilter]);

  const toggleSelection = (num: number) => {
    setSelectedInFilter(prev => 
      prev.includes(num) ? prev.filter(p => p !== num) : [...prev, num].sort((a,b) => a-b)
    );
  };

  const updatePlayer = (playerNo: number, field: keyof Player, value: string) => {
    setPlayers(prev => prev.map(p => p.no === playerNo ? { ...p, [field]: value } : p));
  };

  const addNomination = () => {
    const lastDay = nominations.length > 0 ? nominations[nominations.length - 1].day : 1;
    setNominations([...nominations, { 
      id: Math.random().toString(36).substr(2, 9), 
      day: lastDay, way: '', voters: '', note: '' 
    }]);
  };

  const updateNomination = (id: string, field: keyof Nomination, value: string | number) => {
    setNominations(prev => prev.map(n => n.id === id ? { ...n, [field]: value } : n));
  };

  const toggleVoter = (nominationId: string, playerNo: number) => {
    setNominations(prev => prev.map(n => {
      if (n.id !== nominationId) return n;
      const playerStr = playerNo.toString();
      const currentVoters = n.voters.split(',').filter(v => v !== "");
      let nextVoters: string[];
      if (currentVoters.includes(playerStr)) {
        nextVoters = currentVoters.filter(v => v !== playerStr);
      } else {
        nextVoters = [...currentVoters, playerStr].sort((a, b) => parseInt(a) - parseInt(b));
      }
      return { ...n, voters: nextVoters.join(',') };
    }));
  };

  const updateChar = (faction: keyof CharDict, index: number, field: keyof Character, value: string) => {
    setChars(prev => ({
      ...prev,
      [faction]: prev[faction].map((c, i) => i === index ? { ...c, [field]: value } : c)
    }));
  };

  return (
    <div className="fixed inset-0 bg-slate-100 text-slate-900 flex flex-col font-sans text-xs antialiased overflow-hidden">
      
      {/* Reset Confirmation Modal */}
      {showResetConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white rounded-lg shadow-2xl max-w-xs w-full overflow-hidden border border-slate-200">
            <div className="bg-red-50 p-4 flex flex-col items-center text-center">
              <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mb-3">
                <AlertTriangle className="text-red-600" size={20} />
              </div>
              <h2 className="text-sm font-black text-slate-900 uppercase">Confirm Full Reset?</h2>
              <p className="text-[10px] text-slate-500 mt-2 leading-relaxed">
                This will wipe all <strong>Players, Votes, and Notes</strong>. 
                Role names will be kept but their statuses will be reset.
              </p>
            </div>
            <div className="flex border-t divide-x divide-slate-100">
              <button onClick={() => setShowResetConfirm(false)} className="flex-1 py-3 text-[10px] font-bold text-slate-400 hover:bg-slate-50 transition-colors uppercase">Cancel</button>
              <button onClick={handleSoftReset} className="flex-1 py-3 text-[10px] font-black text-red-600 hover:bg-red-50 transition-colors uppercase">Reset All</button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="bg-slate-900 text-white px-3 py-2 flex justify-between items-center z-30 shadow-lg flex-none">
        <div className="flex items-center gap-1.5">
          <ShieldAlert className="text-red-500" size={14} />
          <h1 className="font-black text-xs tracking-tighter uppercase italic">Ledger v2.3</h1>
        </div>
        <div className="flex gap-2">
          <button 
            title="Full Reset"
            onClick={() => setShowResetConfirm(true)} 
            className="flex items-center gap-1 bg-slate-700 hover:bg-red-900 text-[9px] px-2 py-0.5 rounded transition-colors border border-slate-600 font-bold uppercase"
          >
            <RefreshCcw size={10} /> Full Reset
          </button>
          <button onClick={() => window.location.reload()} className="p-1 text-slate-400 hover:text-white"><RotateCcw size={12} /></button>
          <button className="bg-red-600 text-white px-3 py-0.5 rounded text-[10px] font-black shadow-sm active:scale-95 transition-all">SAVE</button>
        </div>
      </header>

      {/* Tabs */}
      <nav className="bg-white border-b flex z-20 shadow-sm flex-none">
        {[
          { id: 'players', icon: Users, label: 'PLAYERS' },
          { id: 'votes', icon: Vote, label: 'VOTES' },
          { id: 'chars', icon: ShieldAlert, label: 'ROLES' },
          { id: 'notes', icon: FileText, label: 'NOTES' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex-1 flex items-center justify-center gap-1 py-3 text-[9px] font-black transition-all relative ${
              activeTab === tab.id ? 'text-red-600 bg-red-50/50' : 'text-slate-400 hover:text-slate-600'
            }`}
          >
            <tab.icon size={11} />
            <span>{tab.label}</span>
            {activeTab === tab.id && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-red-600" />}
          </button>
        ))}
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-2 bg-slate-100 no-scrollbar">
        <div className="max-w-2xl mx-auto pb-10">
          
          {/* PLAYERS TAB */}
          {activeTab === 'players' && (
            <div className="bg-white rounded border shadow-sm overflow-hidden">
              <table className="w-full text-left border-collapse table-fixed">
                <thead className="bg-slate-50 border-b text-[8px] uppercase text-slate-400 font-black">
                  <tr>
                    <th className="px-2 py-1.5 w-10 text-center cursor-pointer" onClick={() => requestSort('no')}>
                      <div className="flex items-center justify-center gap-0.5"># {getSortIcon('no')}</div>
                    </th>
                    <th className="px-1 py-1.5 w-10 text-center cursor-pointer border-l border-slate-100" onClick={() => requestSort('day')}>
                      <div className="flex flex-col items-center"><Calendar size={10} />{getSortIcon('day')}</div>
                    </th>
                    <th className="px-1 py-1.5 w-10 text-center cursor-pointer border-l border-slate-100" onClick={() => requestSort('reason')}>
                      <div className="flex flex-col items-center"><Zap size={10} />{getSortIcon('reason')}</div>
                    </th>
                    <th className="px-3 py-1.5 cursor-pointer border-l border-slate-100" onClick={() => requestSort('inf')}>
                      <div className="flex items-center gap-0.5">NAME/INFO {getSortIcon('inf')}</div>
                    </th>
                    <th className="px-1 py-1.5 w-10 text-center text-red-500 cursor-pointer border-l border-slate-100" onClick={() => requestSort('red')}>
                      <div className="flex flex-col items-center"><Skull size={10} />{getSortIcon('red')}</div>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {sortedPlayers.map((p) => (
                    <tr key={p.no} className="align-top hover:bg-slate-50/50 transition-colors">
                      <td className="px-2 py-2 text-center text-slate-300 font-mono text-[10px]">{p.no}</td>
                      <td className="border-l border-slate-50">
                        <textarea className="w-full text-center bg-transparent border-none p-2 text-xs font-mono resize-none focus:ring-0 overflow-hidden" rows={1} value={p.day} onChange={(e) => updatePlayer(p.no, 'day', e.target.value)} />
                      </td>
                      <td className="border-l border-slate-50">
                        <textarea className="w-full text-center bg-transparent border-none p-2 text-xs font-mono resize-none focus:ring-0 overflow-hidden" rows={1} value={p.reason} onChange={(e) => updatePlayer(p.no, 'reason', e.target.value)} />
                      </td>
                      <td className="px-1 py-1 border-l border-slate-50">
                        <textarea 
                          className="w-full bg-transparent border-none p-1 text-xs leading-tight resize-none min-h-[1.5rem] focus:ring-0 placeholder:text-slate-200 overflow-hidden"
                          rows={1}
                          value={p.inf}
                          placeholder="..."
                          onChange={(e) => updatePlayer(p.no, 'inf', e.target.value)}
                          onInput={(e) => {
                            const target = e.target as HTMLTextAreaElement;
                            target.style.height = 'auto';
                            target.style.height = target.scrollHeight + 'px';
                          }}
                        />
                      </td>
                      <td className="border-l border-slate-50">
                        <textarea className="w-full text-center bg-transparent border-none p-2 text-xs font-black text-red-600 resize-none focus:ring-0 overflow-hidden" rows={1} value={p.red} onChange={(e) => updatePlayer(p.no, 'red', e.target.value)} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* VOTES TAB */}
          {activeTab === 'votes' && (
            <div className="space-y-2">
              <div className="bg-white p-2 rounded border shadow-sm flex flex-wrap items-center gap-2">
                <span className="text-[9px] font-black text-slate-400 uppercase">Voter Filter:</span>
                <div className="flex flex-wrap gap-1">
                  {Array.from({ length: INITIAL_PLAYERS }, (_, i) => i + 1).map(num => (
                    <button key={num} onClick={() => toggleSelection(num)} className={`w-6 h-6 rounded flex items-center justify-center text-[10px] font-bold border transition-all ${selectedInFilter.includes(num) ? 'bg-blue-600 border-blue-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-400 hover:bg-slate-200'}`}>{num}</button>
                  ))}
                </div>
                <div className="flex gap-1 ml-auto">
                  {selectedInFilter.length > 0 && <button onClick={() => { setSelectedInFilter([]); setActiveFilter([]); }} className="p-1 text-slate-400 hover:text-red-500 transition-colors"><X size={16} /></button>}
                  <button onClick={() => setActiveFilter([...selectedInFilter])} className="flex items-center gap-1 bg-slate-900 text-white px-3 py-1.5 rounded text-[9px] font-black hover:bg-blue-700 transition-all shadow-sm"><Filter size={10} /> {activeFilter.length > 0 ? 'CLEAR' : 'APPLY'}</button>
                </div>
              </div>

              <div className="flex justify-end pt-1">
                <button onClick={addNomination} className="flex items-center gap-1 text-[9px] bg-red-600 text-white px-4 py-1.5 rounded font-black hover:bg-red-700 uppercase shadow-md active:scale-95 transition-all"><Plus size={10} /> Add Nomination</button>
              </div>
              
              <div className="bg-white rounded border shadow-sm overflow-x-auto">
                <table className="w-full border-collapse table-fixed min-w-[500px]">
                  <thead>
                    <tr className="bg-slate-100 border-b text-[8px] uppercase text-slate-500 font-black">
                      <th className="w-8 py-2 border-r text-center">D</th>
                      <th className="w-16 py-2 border-r text-center">F-T</th>
                      <th className="p-0"><div className="flex h-full">{visiblePlayerNumbers.map(num => (<div key={num} className="flex-1 border-r border-slate-200 text-center py-2 text-slate-900 bg-slate-200/50">{num}</div>))}</div></th>
                      <th className="w-32 py-2 text-left px-2">NOTES</th>
                      <th className="w-8 py-2"></th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {nominations.map((n) => (
                      <tr key={n.id} className="hover:bg-slate-50/50 transition-colors">
                        <td className="p-0 border-r border-slate-100"><input type="number" className="w-full text-center border-none bg-transparent focus:ring-0 font-mono text-[10px] p-0 h-8 font-bold" value={n.day} onChange={(e) => updateNomination(n.id, 'day', parseInt(e.target.value) || 1)} /></td>
                        <td className="p-0 border-r border-slate-100"><input placeholder="0-0" className="w-full border-none bg-transparent focus:ring-0 text-[10px] font-bold p-0 text-center tracking-tighter h-8" value={n.way} onChange={(e) => updateNomination(n.id, 'way', e.target.value)} /></td>
                        <td className="p-0"><div className="flex h-8">{visiblePlayerNumbers.map((num) => { const isActive = n.voters.split(',').includes(num.toString()); return (<button key={num} onClick={() => toggleVoter(n.id, num)} className={`flex-1 border-r border-slate-50 h-full flex items-center justify-center text-[9px] font-black transition-all ${isActive ? 'bg-red-600 text-white' : 'bg-white text-transparent hover:bg-slate-100 hover:text-slate-300'}`}>{isActive ? 'V' : num}</button>); })}</div></td>
                        <td className="p-0 border-l border-slate-100"><input placeholder="..." className="w-full border-none bg-transparent focus:ring-0 text-[9px] italic text-slate-400 px-2 h-8 truncate" value={n.note} onChange={(e) => updateNomination(n.id, 'note', e.target.value)} /></td>
                        <td className="p-0 text-center border-l border-slate-100"><button onClick={() => setNominations(prev => prev.filter(nom => nom.id !== n.id))} className="text-slate-200 hover:text-red-500 transition-colors"><Trash2 size={12} /></button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* ROLES TAB */}
          {activeTab === 'chars' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
              {(Object.entries(chars) as [keyof CharDict, Character[]][]).map(([faction, list]) => (
                <div key={faction} className="space-y-1">
                  <h3 className="font-black text-[8px] text-slate-400 uppercase tracking-tighter px-1">{faction}s</h3>
                  <div className="bg-white rounded border shadow-sm">
                    <table className="w-full text-[10px]">
                      <tbody className="divide-y divide-slate-100">
                        {list.map((c, i) => (
                          <tr key={i} className="hover:bg-slate-50 transition-colors">
                            <td className="px-2 py-0"><input className="w-full bg-transparent border-none p-0 h-7 text-[10px]" placeholder="..." value={c.name} onChange={(e) => updateChar(faction, i, 'name', e.target.value)} /></td>
                            <td className="px-0 py-0 border-l border-slate-50 w-8">
                              <select className="w-full bg-transparent border-none p-0 h-7 text-[10px] font-bold text-center appearance-none" value={c.status} onChange={(e) => updateChar(faction, i, 'status', e.target.value as any)}>
                                <option value="0">0</option><option value="1">1</option><option value="2">2</option>
                              </select>
                            </td>
                            <td className="px-2 py-0 border-l border-slate-50"><input className="w-full bg-transparent border-none p-0 h-7 text-[9px] text-slate-400 italic" value={c.note} onChange={(e) => updateChar(faction, i, 'note', e.target.value)} /></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* NOTES TAB */}
          {activeTab === 'notes' && (
            <div className="bg-white rounded border p-4 shadow-sm min-h-[300px]">
              <textarea 
                ref={notesTextareaRef}
                className="w-full border-none focus:ring-0 p-0 text-slate-700 resize-none text-[11px] leading-relaxed font-mono overflow-hidden"
                placeholder="Start recording social reads..."
                value={note}
                onChange={(e) => setNote(e.target.value)}
              />
            </div>
          )}

        </div>
      </main>

      {/* Progress Footer */}
      <div className="fixed bottom-0 left-0 right-0 h-1 bg-slate-300 z-30">
        <div className="h-full bg-red-600 transition-all duration-300 shadow-[0_0_10px_rgba(220,38,38,0.5)]" style={{ width: `${(players.filter(p => p.inf).length / INITIAL_PLAYERS) * 100}%` }} />
      </div>
    </div>
  );
}