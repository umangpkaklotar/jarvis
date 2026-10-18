export function activateJarvis(setStatus) {
    setStatus('Jarvis Activated...');

    const speech = new SpeechSynthesisUtterance('Hello Sir, Jarvis Activated');
    speech.lang = 'en-US';
    window.speechSynthesis.speak(speech);
}