#!/bin/bash

# Definiere den Pfad zum website-Ordner
website_folder="./Website"

# Erstelle den website-Ordner, falls er noch nicht existiert
mkdir -p "$website_folder"

# Erstelle Testdateien in dem website-Ordner
echo '<!DOCTYPE html>
<html>
<head>
    <title>Testseite</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Hello, Salem!</h1>
    <p>Dies ist eine Testseite für das Projekt Salem.</p>
    <script src="script.js"></script>
</body>
</html>' > "$website_folder/index.html"

echo 'body {
    font-family: Arial, sans-serif;
}' > "$website_folder/style.css"

echo 'console.log("Hello, Salem from JS!");' > "$website_folder/script.js"

echo '<?php
echo "Hello, Salem from PHP!";
?>' > "$website_folder/test.php"

# Feedback an den Nutzer
echo "Website-Ordner wurde mit Testdateien vorbereitet."
