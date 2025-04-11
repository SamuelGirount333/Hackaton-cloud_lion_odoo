from odoo import http
from odoo.http import request
import tempfile
import whisper

class VoiceController(http.Controller):

    @http.route('/voice/upload_procedure', type='http', auth='user', methods=['POST'], csrf=False)
    def voice_upload_procedure(self, **kwargs):
        audio_file = request.httprequest.files.get('voice')
        record_id = request.httprequest.form.get('record_id')

        if audio_file and record_id:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
                audio_file.save(temp.name)
                model = whisper.load_model("base")
                result = model.transcribe(temp.name)
                transcription = result["text"]

                # Actualiza el campo de tu modelo
                record = request.env['state.surgery.procedure'].sudo().browse(int(record_id))
                if record:
                    record.write({'voiz_note_description': transcription})

        return "OK"
