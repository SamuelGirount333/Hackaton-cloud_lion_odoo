odoo.define('salud_total.voice_capture', function (require) {
    const ajax = require('web.ajax');

    let recorder;
    let chunks = [];

    document.addEventListener('DOMContentLoaded', function () {
        const btn = document.getElementById('record-procedure-btn');
        const status = document.getElementById('voice-status');
        if (!btn) return;

        btn.addEventListener('click', async () => {
            if (!recorder || recorder.state === "inactive") {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                recorder = new MediaRecorder(stream);
                chunks = [];

                recorder.ondataavailable = e => chunks.push(e.data);
                recorder.onstop = async () => {
                    const blob = new Blob(chunks, { type: 'audio/wav' });
                    const formData = new FormData();
                    formData.append('voice', blob);
                    const recordId = document.querySelector('input[name="id"]').value;
                    formData.append('record_id', recordId);

                    status.innerText = "⏳ Procesando...";
                    await fetch('/voice/upload_procedure', { method: 'POST', body: formData });
                    status.innerText = "✅ Transcripción lista";
                };

                recorder.start();
                status.innerText = "🎙️ Grabando... Click otra vez para detener.";
            } else {
                recorder.stop();
            }
        });
    });
});
