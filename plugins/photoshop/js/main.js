// Plugin Photoshop UI Generator
class UIGenerator {
    constructor() {
        this.csInterface = new CSInterface();
        this.currentCode = '';
        this.init();
    }
    
    init() {
        document.getElementById('analyzeBtn').addEventListener('click', () => this.analyzeDocument());
        document.getElementById('copyBtn').addEventListener('click', () => this.copyCode());
        document.getElementById('saveBtn').addEventListener('click', () => this.saveCode());
        document.getElementById('sendBtn').addEventListener('click', () => this.sendToCMDAI());
        document.getElementById('codeFormat').addEventListener('change', () => this.generateCode());
    }
    
    analyzeDocument() {
        const btn = document.getElementById('analyzeBtn');
        btn.textContent = '⏳ Analyse...';
        btn.disabled = true;
        
        this.csInterface.evalScript('exportCurrentDocument()', (result) => {
            if (result === 'error') {
                this.showError('Erreur lors de l\'export du document');
                btn.textContent = '🔍 Analyser le document';
                btn.disabled = false;
                return;
            }
            
            this.analyzeImage(result);
            btn.textContent = '🔍 Analyser le document';
            btn.disabled = false;
        });
    }
    
    analyzeImage(imagePath) {
        const mockResults = {
            elements: [
                { type: 'button', x: 100, y: 50, width: 120, height: 35, properties: { text: 'Button', bg_color: '#E0E0E0', fg_color: '#000000' }},
                { type: 'entry', x: 100, y: 100, width: 200, height: 25, properties: { text: '', bg_color: '#FFFFFF', fg_color: '#000000' }},
                { type: 'label', x: 100, y: 140, width: 80, height: 20, properties: { text: 'Label', bg_color: 'transparent', fg_color: '#000000' }}
            ],
            image_size: [800, 600],
            total_elements: 3
        };
        
        this.displayResults(mockResults);
        this.generateCode(mockResults);
    }
    
    displayResults(results) {
        const resultsDiv = document.getElementById('results');
        let html = `✅ ${results.total_elements} éléments détectés<br>`;
        html += `📐 Taille: ${results.image_size[0]}x${results.image_size[1]}px<br><br>`;
        
        results.elements.forEach((elem, i) => {
            html += `${i+1}. ${elem.type} (${elem.x},${elem.y})<br>`;
        });
        
        resultsDiv.innerHTML = html;
    }
    
    generateCode(results = null) {
        if (!results) return;
        
        const format = document.getElementById('codeFormat').value;
        let code = '';
        
        if (format === 'tkinter') {
            code = this.generateTkinterCode(results);
        } else if (format === 'pyqt') {
            code = this.generatePyQtCode(results);
        } else if (format === 'html') {
            code = this.generateHTMLCode(results);
        }
        
        this.currentCode = code;
        document.getElementById('codeOutput').value = code;
    }
    
    generateTkinterCode(results) {
        return `#!/usr/bin/env python3
import tkinter as tk

class GeneratedInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interface Générée")
        self.root.geometry("${results.image_size[0]}x${results.image_size[1]}")
        self.setup_ui()
    
    def setup_ui(self):
        ${results.elements.map((elem, i) => {
            const props = elem.properties;
            if (elem.type === 'button') {
                return `btn_${i} = tk.Button(self.root, text="${props.text}", bg="${props.bg_color}")
        btn_${i}.place(x=${elem.x}, y=${elem.y}, width=${elem.width}, height=${elem.height})`;
            }
            return '';
        }).join('\n        ')}

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GeneratedInterface()
    app.run()`;
    }
    
    generatePyQtCode(results) {
        return `#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import *

class GeneratedInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface Générée")
        self.setGeometry(100, 100, ${results.image_size[0]}, ${results.image_size[1]})
        self.setup_ui()
    
    def setup_ui(self):
        ${results.elements.map((elem, i) => {
            if (elem.type === 'button') {
                return `btn_${i} = QPushButton("${elem.properties.text}", self)
        btn_${i}.setGeometry(${elem.x}, ${elem.y}, ${elem.width}, ${elem.height})`;
            }
            return '';
        }).join('\n        ')}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratedInterface()
    window.show()
    sys.exit(app.exec_())`;
    }
    
    generateHTMLCode(results) {
        return `<!DOCTYPE html>
<html>
<head>
    <title>Interface Générée</title>
    <style>
        body { margin: 0; position: relative; width: ${results.image_size[0]}px; height: ${results.image_size[1]}px; }
        .element { position: absolute; }
    </style>
</head>
<body>
    ${results.elements.map((elem, i) => {
        if (elem.type === 'button') {
            return `<button class="element" style="left: ${elem.x}px; top: ${elem.y}px; width: ${elem.width}px; height: ${elem.height}px;">${elem.properties.text}</button>`;
        }
        return '';
    }).join('\n    ')}
</body>
</html>`;
    }
    
    copyCode() {
        if (this.currentCode) {
            navigator.clipboard.writeText(this.currentCode);
            this.showInfo('Code copié!');
        }
    }
    
    saveCode() {
        if (!this.currentCode) return;
        
        this.csInterface.evalScript(`saveCodeToFile("${this.currentCode.replace(/"/g, '\\"')}")`, (result) => {
            this.showInfo(result === 'success' ? 'Code sauvegardé!' : 'Erreur sauvegarde');
        });
    }
    
    sendToCMDAI() {
        if (!this.currentCode) return;
        
        this.csInterface.evalScript(`sendToCMDAI("${this.currentCode.replace(/"/g, '\\"')}")`, (result) => {
            this.showInfo(result === 'success' ? 'Code envoyé vers CMD-AI!' : 'CMD-AI non détecté');
        });
    }
    
    showError(message) { alert('❌ ' + message); }
    showInfo(message) { alert('✅ ' + message); }
}

document.addEventListener('DOMContentLoaded', () => new UIGenerator());