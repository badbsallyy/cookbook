# Gemini Agent Cookbook / Leitfaden

Dies ist ein vereinfachter Leitfaden für die Entwicklung von LLM-Agents mit dem Gemini API.

**Über dieses Repository:**
* Dies ist eine vereinfachte Version des [Original Gemini API Cookbook](https://github.com/google-gemini/cookbook)
* Optimiert für LLM-lesbare Formate und fokussiert auf Agent-Entwicklung
* Enthält Python-basierte Quickstarts und praktische Beispiele

**Für umfassende API-Dokumentation, besuchen Sie [ai.google.dev](https://ai.google.dev/gemini-api/docs).**
<br><br>

## Navigation / Übersicht

Dieses Repository ist in zwei Hauptkategorien organisiert:

1.  **[Quick Starts](./quickstarts/):**  Schritt-für-Schritt-Anleitungen zu Einführungsthemen und spezifischen API-Features.
2.  **[Examples](./examples/):** Praktische Anwendungsfälle, die zeigen, wie man mehrere Features kombiniert.

<br><br>



## 1. Quick Starts

Der [quickstarts Ordner](./quickstarts/) enthält Schritt-für-Schritt-Tutorials, um mit Gemini zu beginnen und spezifische Features kennenzulernen.

**Um zu starten, benötigen Sie:**

1.  Ein Google-Konto
2.  Einen API-Key (erstellen Sie einen in [Google AI Studio](https://aistudio.google.com/app/apikey))

**Empfohlener Einstieg:**

*   [Authentication](./quickstarts/Authentication.ipynb): API-Key einrichten
*   [Get started](./quickstarts/Get_started.ipynb): Erste Schritte mit Gemini-Modellen und der API

**Weitere wichtige Quickstarts:**
*  [Get started with Live API](./quickstarts/Get_started_LiveAPI.ipynb): Multimodale Live API
*  [Function Calling](./quickstarts/Function_calling.ipynb): Funktionsaufrufe für Agent-Entwicklung
*  [Code Execution](./quickstarts/Code_Execution.ipynb): Python-Code generieren und ausführen
*  [Grounding](./quickstarts/Grounding.ipynb): Antworten mit Google Search verankern
*  [System Instructions](./quickstarts/System_instructions.ipynb): Systemanweisungen für Agents
*  Und [viele weitere](./quickstarts/)
<br><br>

## 2. Examples (Praktische Anwendungsfälle)

Der [examples Ordner](./examples/) zeigt, wie man mehrere Gemini API Features oder Drittanbieter-Tools kombiniert, um komplexere Anwendungen zu erstellen.

**Beispiele für Agent-Entwicklung:**
*  [Agents Function Calling Barista Bot](./examples/Agents_Function_Calling_Barista_Bot.ipynb): Agent mit Function Calling
*  [Browser as a tool](./examples/Browser_as_a_tool.ipynb): Webbrowser als Tool für Agents
*  [Search Re-ranking](./examples/Search_reranking_using_embeddings.ipynb): Suchranking mit Embeddings
*  [JSON Capabilities](./examples/json_capabilities/): Strukturierte Outputs
*  [Prompting](./examples/prompting/): Verschiedene Prompting-Techniken

**Weitere Beispiele:**
*  [Video Analysis](./examples/Analyze_a_Video_Summarization.ipynb): Video-Analyse und -Zusammenfassung
*  [Spatial Understanding](./examples/Spatial_understanding_3d.ipynb): 3D-Szenenverständnis
*  Und [viele weitere](./examples/)
<br><br>




## Offizielle SDKs

Die Gemini API ist eine REST API. Sie können sie direkt mit Tools wie `curl` aufrufen (siehe [REST Beispiele](./quickstarts/rest/)) oder eines der offiziellen SDKs verwenden:
* [Python](https://github.com/googleapis/python-genai) (Fokus dieses Repositories)
* [Go](https://github.com/google/generative-ai-go)
* [Node.js](https://github.com/google/generative-ai-js)
* Weitere: Dart, Android, Swift
<br><br>

## Ressourcen

* **Original Repository:** [google-gemini/cookbook](https://github.com/google-gemini/cookbook)
* **API Dokumentation:** [ai.google.dev](https://ai.google.dev/gemini-api/docs)
* **Forum:** [Google AI Developer Forum](https://discuss.ai.google.dev/)
* **Vertex AI:** Für Enterprise-Entwickler ist die Gemini API auch auf [Google Cloud Vertex AI](https://github.com/GoogleCloudPlatform/generative-ai) verfügbar

## Über diese Version

Dies ist eine vereinfachte, fokussierte Version des Original-Cookbooks, optimiert für:
* LLM-Agent Entwicklung
* Python-basierte Implementierungen
* Schnellen Zugriff auf relevante Tutorials und Beispiele

Für die vollständige Version mit allen Features, Sprachen und Beiträgen besuchen Sie das [Original-Repository](https://github.com/google-gemini/cookbook).




