// Script ExtendScript pour Photoshop
function exportCurrentDocument() {
    try {
        if (!app.activeDocument) {
            return "error";
        }
        
        var doc = app.activeDocument;
        var tempFile = new File(Folder.temp + "/ps_ui_analysis.png");
        
        // Options d'export PNG
        var pngOptions = new PNGSaveOptions();
        pngOptions.compression = 6;
        pngOptions.interlaced = false;
        
        // Sauvegarder temporairement
        doc.saveAs(tempFile, pngOptions, true, Extension.LOWERCASE);
        
        return tempFile.fsName;
    } catch (e) {
        return "error";
    }
}

function saveCodeToFile(code) {
    try {
        var saveFile = File.saveDialog("Sauvegarder le code", "*.py;*.html");
        if (saveFile) {
            saveFile.open("w");
            saveFile.write(code);
            saveFile.close();
            return "success";
        }
        return "cancelled";
    } catch (e) {
        return "error";
    }
}

function sendToCMDAI(code) {
    try {
        // Créer un fichier temporaire avec le code
        var tempFile = new File(Folder.temp + "/cmdai_generated_code.py");
        tempFile.open("w");
        tempFile.write(code);
        tempFile.close();
        
        // Essayer de lancer CMD-AI avec le fichier
        var cmdaiPath = findCMDAIPath();
        if (cmdaiPath) {
            var command = '"' + cmdaiPath + '" --import "' + tempFile.fsName + '"';
            system.callSystem(command);
            return "success";
        }
        
        return "not_found";
    } catch (e) {
        return "error";
    }
}

function findCMDAIPath() {
    // Chemins possibles de CMD-AI Ultra Reboot
    var possiblePaths = [
        "C:\\Program Files\\CMD-AI Ultra Reboot\\main.exe",
        "C:\\CMD-AI Ultra Reboot\\main.exe",
        "/usr/local/bin/cmd-ai",
        "/Applications/CMD-AI Ultra Reboot.app/Contents/MacOS/main"
    ];
    
    for (var i = 0; i < possiblePaths.length; i++) {
        var file = new File(possiblePaths[i]);
        if (file.exists) {
            return possiblePaths[i];
        }
    }
    
    return null;
}

function getDocumentInfo() {
    try {
        if (!app.activeDocument) {
            return "no_document";
        }
        
        var doc = app.activeDocument;
        var info = {
            name: doc.name,
            width: doc.width.as("px"),
            height: doc.height.as("px"),
            layers: doc.layers.length,
            colorMode: doc.mode
        };
        
        return JSON.stringify(info);
    } catch (e) {
        return "error";
    }
}