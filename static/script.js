function activateJarvis(){

    let status = document.getElementById("status");

    status.innerHTML = "Jarvis Activated...";

    let speech = new SpeechSynthesisUtterance(
        "Hello Sir, Jarvis Activated"
    );

    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);
}