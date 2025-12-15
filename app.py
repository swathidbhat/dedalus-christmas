"""Christmas Riddle Generator - Dedalus + GPT-4o-mini"""
import csv
import io
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse

load_dotenv()

app = FastAPI(title="🎄 Christmas Riddle Generator")
client = AsyncDedalus()
runner = DedalusRunner(client)


async def generate_riddle(gift: str, name: str) -> str:
    """Generate a rhyming Christmas riddle that hints at the gift without revealing it."""
    response = await runner.run(
        input=f"""Create a 4-line rhyming Christmas riddle for {name}.
The gift is: {gift}

Rules:
- NEVER mention the gift name or any obvious synonyms
- Only give clever HINTS about what it does or how it's used
- Make it rhyme (AABB or ABAB pattern)
- Keep it festive and fun
- The reader should have to GUESS what the gift is

Return ONLY the riddle, nothing else.""",
        model="openai/gpt-4o-mini"
    )
    return response.final_output.strip()


@app.get("/", response_class=HTMLResponse)
async def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎄 Christmas Riddle Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Crimson+Text:ital@0;1&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            min-height: 100vh;
            font-family: 'Crimson Text', Georgia, serif;
            background: linear-gradient(135deg, #1a472a 0%, #0d2818 50%, #2d1b1b 100%);
            color: #f5e6d3;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        /* Snowflakes */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                radial-gradient(2px 2px at 20px 30px, #fff, transparent),
                radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
                radial-gradient(1px 1px at 90px 40px, #fff, transparent),
                radial-gradient(2px 2px at 130px 80px, rgba(255,255,255,0.6), transparent),
                radial-gradient(1px 1px at 160px 120px, #fff, transparent);
            background-size: 200px 200px;
            animation: snow 8s linear infinite;
            pointer-events: none;
            opacity: 0.4;
        }
        
        @keyframes snow {
            0% { background-position: 0 0, 0 0, 0 0, 0 0, 0 0; }
            100% { background-position: 200px 200px, 100px 300px, 150px 250px, 50px 400px, 175px 350px; }
        }
        
        .container {
            background: rgba(139, 69, 19, 0.15);
            border: 2px solid rgba(218, 165, 32, 0.3);
            border-radius: 20px;
            padding: 3rem;
            max-width: 600px;
            width: 100%;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            position: relative;
            z-index: 1;
        }
        
        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 50%, #ffd700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
        }
        
        .subtitle {
            text-align: center;
            font-style: italic;
            color: #c4a574;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }
        
        .upload-zone {
            border: 2px dashed rgba(218, 165, 32, 0.5);
            border-radius: 15px;
            padding: 2.5rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            background: rgba(0,0,0,0.2);
        }
        
        .upload-zone:hover {
            border-color: #daa520;
            background: rgba(218, 165, 32, 0.1);
        }
        
        .upload-zone.dragover {
            border-color: #ffd700;
            background: rgba(255, 215, 0, 0.15);
        }
        
        .upload-icon { font-size: 3rem; margin-bottom: 1rem; }
        
        input[type="file"] { display: none; }
        
        .btn {
            display: inline-block;
            margin-top: 1.5rem;
            padding: 1rem 2.5rem;
            background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
            color: #1a1a1a;
            border: none;
            border-radius: 30px;
            font-family: 'Playfair Display', serif;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(218, 165, 32, 0.4); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        
        #status {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            display: none;
        }
        
        #status.loading {
            display: block;
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid rgba(255, 215, 0, 0.3);
        }
        
        #status.success {
            display: block;
            background: rgba(34, 139, 34, 0.2);
            border: 1px solid rgba(34, 139, 34, 0.5);
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255,215,0,0.3);
            border-top-color: #ffd700;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .file-name {
            margin-top: 1rem;
            color: #daa520;
            font-weight: bold;
        }
        
        .format-hint {
            margin-top: 1.5rem;
            font-size: 0.9rem;
            color: #a0a0a0;
            text-align: center;
        }
        
        .format-hint code {
            background: rgba(0,0,0,0.3);
            padding: 2px 8px;
            border-radius: 4px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎄 Christmas Riddles</h1>
        <p class="subtitle">Upload your gift list, receive magical riddles</p>
        
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-zone" id="dropZone">
                <div class="upload-icon">📜</div>
                <p>Drop your CSV here or click to browse</p>
                <div class="file-name" id="fileName"></div>
                <input type="file" id="fileInput" name="file" accept=".csv" required>
            </div>
            
            <div style="text-align: center;">
                <button type="submit" class="btn" id="submitBtn" disabled>
                    ✨ Generate Riddles ✨
                </button>
            </div>
        </form>
        
        <div id="status"></div>
        
        <p class="format-hint">
            CSV format: <code>Name, Gift Idea, Budget</code>
        </p>
    </div>
    
    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const fileName = document.getElementById('fileName');
        const submitBtn = document.getElementById('submitBtn');
        const status = document.getElementById('status');
        const form = document.getElementById('uploadForm');
        
        dropZone.addEventListener('click', () => fileInput.click());
        
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
        
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileName();
            }
        });
        
        fileInput.addEventListener('change', updateFileName);
        
        function updateFileName() {
            if (fileInput.files.length) {
                fileName.textContent = '📎 ' + fileInput.files[0].name;
                submitBtn.disabled = false;
            }
        }
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            submitBtn.disabled = true;
            status.className = 'loading';
            status.innerHTML = '<span class="spinner"></span> Generating riddles... This may take a minute ✨';
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'christmas_riddles.csv';
                    a.click();
                    window.URL.revokeObjectURL(url);
                    
                    status.className = 'success';
                    status.innerHTML = '🎁 Riddles generated! Check your downloads folder.';
                } else {
                    throw new Error('Generation failed');
                }
            } catch (error) {
                status.className = 'loading';
                status.innerHTML = '❌ Error: ' + error.message;
            }
            
            submitBtn.disabled = false;
        });
    </script>
</body>
</html>"""


@app.post("/generate")
async def generate_riddles(file: UploadFile = File(...)):
    """Process CSV and generate riddles for each gift."""
    # Read uploaded CSV
    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(io.StringIO(text))
    
    # Process each row
    results = []
    for row in reader:
        name = row.get('Name', '').strip()
        gift = row.get('Gift Idea', '').strip()
        budget = row.get('Budget', '').strip()
        
        if not name or not gift:
            continue
        
        print(f"🎁 Generating riddle for {name}...")
        riddle = await generate_riddle(gift, name)
        
        results.append({
            'Name': name,
            'Gift Idea': gift,
            'Budget': budget,
            'Riddle': riddle
        })
    
    # Create output CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['Name', 'Gift Idea', 'Budget', 'Riddle'])
    writer.writeheader()
    writer.writerows(results)
    
    # Return as downloadable file
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=christmas_riddles.csv'}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
