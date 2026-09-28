import React,{useEffect,useState} from "react";
import {createRoot} from "react-dom/client";
import "./styles.css";

const API=import.meta.env.VITE_API_URL||"http://localhost:8000/api";
const WS=import.meta.env.VITE_WS_URL||"ws://localhost:8000/api/ws/events";

async function api(path,opts={}){
  const token=localStorage.getItem("token");
  const headers={"Content-Type":"application/json",...(opts.headers||{})};
  if(token) headers.Authorization=`Bearer ${token}`;
  const r=await fetch(`${API}${path}`,{...opts,headers});
  const data=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(data.detail||"Request failed");
  return data;
}

function Auth({onLogin}){
  const [mode,setMode]=useState("login");
  const [form,setForm]=useState({name:"",email:"",password:"",role:"ATTENDEE"});
  const [error,setError]=useState("");
  const submit=async e=>{e.preventDefault();setError("");
    try{const d=await api(mode==="login"?"/login":"/register",{method:"POST",body:JSON.stringify(form)});
      localStorage.setItem("token",d.access_token);localStorage.setItem("user",JSON.stringify(d.user));onLogin(d.user);
    }catch(x){setError(x.message)}
  };
  return <div className="auth"><div className="card"><h1>☁ EventFlow</h1><p>Real-Time Cloud Event Planning & RSVP</p>
    <form onSubmit={submit}>{mode==="register"&&<input placeholder="Name" required onChange={e=>setForm({...form,name:e.target.value})}/>}
    <input type="email" placeholder="Email" required onChange={e=>setForm({...form,email:e.target.value})}/>
    <input type="password" placeholder="Password" required onChange={e=>setForm({...form,password:e.target.value})}/>
    {mode==="register"&&<select onChange={e=>setForm({...form,role:e.target.value})}><option>ATTENDEE</option><option>ORGANIZER</option></select>}
    {error&&<div className="error">{error}</div>}<button>{mode==="login"?"Login":"Create account"}</button></form>
    <button className="link" onClick={()=>setMode(mode==="login"?"register":"login")}>{mode==="login"?"Need an account? Register":"Already registered? Login"}</button>
  </div></div>
}

function App(){
  const [user,setUser]=useState(()=>JSON.parse(localStorage.getItem("user")||"null"));
  const [events,setEvents]=useState([]); const [selected,setSelected]=useState(null);
  const [message,setMessage]=useState(""); const [showCreate,setShowCreate]=useState(false);
  const load=()=>api("/events").then(setEvents).catch(e=>setMessage(e.message));
  useEffect(()=>{if(user)load()},[user]);
  useEffect(()=>{if(!selected)return;const ws=new WebSocket(`${WS}/${selected.id}`);
    ws.onmessage=e=>{const d=JSON.parse(e.data); if(d.type==="rsvp_update"){setSelected(s=>({...s,counts:d.counts,status:d.status,available_capacity:d.available_capacity}));load()}
      if(d.type==="announcement") setMessage(`📢 ${d.title}: ${d.message}`)};
    return()=>ws.close()
  },[selected?.id]);
  if(!user)return <Auth onLogin={setUser}/>;
  const logout=()=>{localStorage.clear();setUser(null)};
  const rsvp=async(status)=>{try{const d=await api(`/events/${selected.id}/rsvp`,{method:"POST",body:JSON.stringify({status})});setSelected(s=>({...s,...d}));setMessage("Your RSVP has been recorded.")}catch(e){setMessage(e.message)}};
  const create=async(e)=>{e.preventDefault();const f=new FormData(e.target);const body=Object.fromEntries(f.entries());
    body.maximum_capacity=Number(body.maximum_capacity);try{await api("/events",{method:"POST",body:JSON.stringify(body)});setShowCreate(false);e.target.reset();load()}catch(x){setMessage(x.message)}};
  return <div><header><div><b>☁ EventFlow</b><span className="pill">CLOUD + REAL-TIME</span></div>
    <div>{user.name} · {user.role}<button className="small" onClick={logout}>Logout</button></div></header>
    <main><section className="hero"><h1>Event Planning, built for the cloud.</h1><p>Live RSVP counters, role-based access, announcements and analytics.</p>
    {user.role!=="ATTENDEE"&&<button onClick={()=>setShowCreate(true)}>+ Create Event</button>}</section>
    {message&&<div className="notice">{message}<button onClick={()=>setMessage("")}>×</button></div>}
    <div className="grid">{events.map(e=><article className="event" key={e.id}><div className="eventtop"><span className="pill">{e.status}</span><span>{e.event_type}</span></div>
      <h2>{e.event_name}</h2><p>{e.description}</p><p>📅 {e.event_date} · {e.start_time}–{e.end_time}</p><p>📍 {e.venue||"Online"}</p>
      <div className="counts"><b>🟢 {e.counts.GOING}</b><b>🟡 {e.counts.MAYBE}</b><b>⚪ {e.counts.NOT_GOING}</b><span>{e.available_capacity} seats left</span></div>
      <button onClick={()=>setSelected(e)}>View / RSVP</button></article>)}</div>
    </main>
    {selected&&<div className="modal"><div className="card wide"><button className="close" onClick={()=>setSelected(null)}>×</button><h2>{selected.event_name}</h2><p>{selected.description}</p>
      <div className="stats"><div><strong>{selected.counts.GOING}</strong><small>Going</small></div><div><strong>{selected.counts.MAYBE}</strong><small>Maybe</small></div><div><strong>{selected.counts.NOT_GOING}</strong><small>Not Going</small></div></div>
      <div className="actions"><button onClick={()=>rsvp("GOING")}>GOING</button><button onClick={()=>rsvp("MAYBE")}>MAYBE</button><button onClick={()=>rsvp("NOT_GOING")}>NOT GOING</button></div>
      <p className="muted">The organizer dashboard receives updates through WebSocket without a manual refresh.</p></div></div>}
    {showCreate&&<div className="modal"><form className="card wide" onSubmit={create}><button type="button" className="close" onClick={()=>setShowCreate(false)}>×</button><h2>Create Event</h2>
      <input name="event_name" placeholder="Event name" required/><textarea name="description" placeholder="Description"/><input name="event_type" placeholder="Type" defaultValue="Workshop"/>
      <div className="row"><input name="event_date" type="date" required/><input name="start_time" type="time" required/><input name="end_time" type="time" required/></div>
      <input name="venue" placeholder="Venue / meeting room"/><input name="online_link" placeholder="Optional online link"/>
      <div className="row"><input name="maximum_capacity" type="number" min="1" defaultValue="100" required/><input name="registration_deadline" type="datetime-local" required/></div>
      <button>Create Event</button></form></div>}
  </div>
}
createRoot(document.getElementById("root")).render(<App/>);
