const $ = id => document.getElementById(id);
let voices = [];

function load() {
    voices = speechSynthesis.getVoices();
    $('voice').innerHTML = voices.map((voice, index) => 
    `<option value="${index}">${voice.name}</option>`).join('');
}
speechSynthesis.onvoiceschanged = load;
load();

$('speak').onclick = () => {
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance($('text').value);
    u.voice = voices[$('voice').value];
    u.rate = $('rate').value;
    speechSynthesis.speak(u);
};

$('stop').onclick = () => {
    speechSynthesis.cancel();
};