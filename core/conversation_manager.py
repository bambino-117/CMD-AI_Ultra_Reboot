import json
import os
from datetime import datetime
import webbrowser
import tempfile
from core.logger import app_logger

# Import sécurisé de reportlab
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    HAS_REPORTLAB = True
    app_logger.debug("ReportLab importé avec succès", "CONVERSATION_MANAGER")
except ImportError as e:
    HAS_REPORTLAB = False
    app_logger.warning(f"ReportLab non disponible: {e}", "CONVERSATION_MANAGER")
    canvas = None
    letter = None

class ConversationManager:
    def __init__(self):
        self.conversations_dir = "user/conversations"
        self.exports_dir = "user/exports"
        os.makedirs(self.conversations_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)
    
    def save_conversation(self, messages, title=None):
        """Sauvegarde une conversation"""
        try:
            if not title:
                title = f"Conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            conversation_data = {
                "title": title,
                "created_at": datetime.now().isoformat(),
                "messages": messages,
                "message_count": len(messages)
            }
            
            filename = f"{title.replace(' ', '_')}.json"
            filepath = os.path.join(self.conversations_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            return f"✅ Conversation sauvegardée: {title}"
            
        except Exception as e:
            app_logger.error(f"Erreur sauvegarde conversation: {e}", "CONV_MANAGER")
            return f"❌ Erreur sauvegarde: {e}"
    
    def list_conversations(self):
        """Liste les conversations sauvegardées"""
        try:
            files = [f for f in os.listdir(self.conversations_dir) if f.endswith('.json')]
            
            if not files:
                return "📂 Aucune conversation sauvegardée\n💡 Utilisez 'conv save' pour sauvegarder"
            
            result = "💬 CONVERSATIONS SAUVEGARDÉES\n\n"
            
            for file in sorted(files, reverse=True):
                filepath = os.path.join(self.conversations_dir, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    title = data.get('title', file[:-5])
                    created = data.get('created_at', '')[:10]
                    count = data.get('message_count', 0)
                    
                    result += f"📄 {title}\n"
                    result += f"   📅 {created} | 💬 {count} messages\n"
                    result += f"   📖 Ouvrir: conv load {title}\n"
                    result += f"   📄 Export PDF: conv pdf {title}\n\n"
                    
                except:
                    continue
            
            return result
            
        except Exception as e:
            return f"❌ Erreur: {e}"
    
    def load_conversation(self, title):
        """Charge une conversation"""
        try:
            filename = f"{title.replace(' ', '_')}.json"
            filepath = os.path.join(self.conversations_dir, filename)
            
            if not os.path.exists(filepath):
                return f"❌ Conversation '{title}' non trouvée"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            result = f"📖 CONVERSATION: {data['title']}\n"
            result += f"📅 Créée le: {data['created_at'][:10]}\n\n"
            
            for i, msg in enumerate(data['messages'], 1):
                result += f"[{i}] Vous: {msg.get('user', '')}\n"
                result += f"[{i}] IA: {msg.get('ai', '')}\n\n"
            
            return result
            
        except Exception as e:
            return f"❌ Erreur chargement: {e}"
    
    def export_to_pdf(self, title):
        """Exporte une conversation en PDF"""
        try:
            if not HAS_REPORTLAB:
                return "❌ Exportation PDF non disponible (reportlab manquant)\n" + \
                       "💡 Installer avec: pip install reportlab"
            
            filename = f"{title.replace(' ', '_')}.json"
            filepath = os.path.join(self.conversations_dir, filename)
            
            if not os.path.exists(filepath):
                return f"❌ Conversation '{title}' non trouvée"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Créer le PDF
            pdf_filename = f"{title.replace(' ', '_')}.pdf"
            pdf_path = os.path.join(self.exports_dir, pdf_filename)
            
            c = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter
            
            # Titre
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, f"Conversation: {data['title']}")
            
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 70, f"Créée le: {data['created_at'][:10]}")
            c.drawString(50, height - 85, f"Messages: {data['message_count']}")
            
            # Messages
            y_position = height - 120
            c.setFont("Helvetica", 9)
            
            for i, msg in enumerate(data['messages'], 1):
                if y_position < 100:  # Nouvelle page
                    c.showPage()
                    y_position = height - 50
                
                # Message utilisateur
                user_text = f"[{i}] Vous: {msg.get('user', '')}"
                c.drawString(50, y_position, user_text[:80])
                y_position -= 15
                
                # Message IA
                ai_text = f"[{i}] IA: {msg.get('ai', '')}"
                # Découper le texte long
                words = ai_text.split()
                line = ""
                for word in words:
                    if len(line + word) < 80:
                        line += word + " "
                    else:
                        c.drawString(70, y_position, line)
                        y_position -= 12
                        line = word + " "
                        if y_position < 100:
                            c.showPage()
                            y_position = height - 50
                
                if line:
                    c.drawString(70, y_position, line)
                    y_position -= 20
            
            c.save()
            
            return f"✅ PDF exporté: {pdf_path}\n📂 Dossier: {self.exports_dir}"
            
        except Exception as e:
            app_logger.error(f"Erreur export PDF: {e}", "CONV_MANAGER")
            return f"❌ Erreur export PDF: {e}"
    
    def export_to_html(self, title):
        """Exporte une conversation en HTML"""
        try:
            filename = f"{title.replace(' ', '_')}.json"
            filepath = os.path.join(self.conversations_dir, filename)
            
            if not os.path.exists(filepath):
                return f"❌ Conversation '{title}' non trouvée"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Créer le HTML
            html_filename = f"{title.replace(' ', '_')}.html"
            html_path = os.path.join(self.exports_dir, html_filename)
            
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{data['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .message {{ margin: 20px 0; padding: 10px; border-radius: 5px; }}
        .user {{ background-color: #e3f2fd; }}
        .ai {{ background-color: #f3e5f5; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{data['title']}</h1>
        <p class="timestamp">Créée le: {data['created_at'][:10]} | Messages: {data['message_count']}</p>
    </div>
"""
            
            for i, msg in enumerate(data['messages'], 1):
                html_content += f"""
    <div class="message user">
        <strong>[{i}] Vous:</strong> {msg.get('user', '')}
    </div>
    <div class="message ai">
        <strong>[{i}] IA:</strong> {msg.get('ai', '')}
    </div>
"""
            
            html_content += """
</body>
</html>"""
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return f"✅ HTML exporté: {html_path}\n🌐 Ouvrir: conv open {title}"
            
        except Exception as e:
            return f"❌ Erreur export HTML: {e}"
    
    def open_in_browser(self, title):
        """Ouvre une conversation dans le navigateur"""
        try:
            html_filename = f"{title.replace(' ', '_')}.html"
            html_path = os.path.join(self.exports_dir, html_filename)
            
            if not os.path.exists(html_path):
                # Créer le HTML d'abord
                result = self.export_to_html(title)
                if result.startswith("❌"):
                    return result
            
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
            return f"🌐 Conversation ouverte dans le navigateur"
            
        except Exception as e:
            return f"❌ Erreur ouverture: {e}"
    
    def delete_conversation(self, title):
        """Supprime une conversation"""
        try:
            filename = f"{title.replace(' ', '_')}.json"
            filepath = os.path.join(self.conversations_dir, filename)
            
            if not os.path.exists(filepath):
                return f"❌ Conversation '{title}' non trouvée"
            
            os.remove(filepath)
            
            # Supprimer aussi les exports
            html_path = os.path.join(self.exports_dir, f"{title.replace(' ', '_')}.html")
            pdf_path = os.path.join(self.exports_dir, f"{title.replace(' ', '_')}.pdf")
            
            if os.path.exists(html_path):
                os.remove(html_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            
            return f"✅ Conversation '{title}' supprimée"
            
        except Exception as e:
            return f"❌ Erreur suppression: {e}"