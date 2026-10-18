import { useState } from 'react';
import { activateJarvis } from './script.js';

export default function App() {
  const [status, setStatus] = useState('Waiting for command...');

  return (
    <main className="container">
      <h1>JARVIS AI</h1>
      <p id="status" aria-live="polite">{status}</p>
      <div className="circle" aria-hidden="true">
        <div className="mic" />
      </div>
      <button type="button" onClick={() => activateJarvis(setStatus)}>
        Activate Jarvis
      </button>
    </main>
  );
}
