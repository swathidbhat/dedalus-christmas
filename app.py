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
    <title>The Riddle Workshop</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --neon-gold: #ffd700;
            --neon-red: #ff2d55;
            --neon-cyan: #00f0ff;
            --void: #030306;
            --surface: rgba(255,255,255,0.03);
        }
        
        body {
            min-height: 100vh;
            font-family: 'IBM Plex Mono', monospace;
            background: var(--void);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        
        /* Animated grid background */
        .grid-bg {
            position: fixed;
            inset: 0;
            background-image: 
                linear-gradient(rgba(255,215,0,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,215,0,0.03) 1px, transparent 1px);
            background-size: 60px 60px;
            animation: grid-move 20s linear infinite;
            z-index: 0;
        }
        
        @keyframes grid-move {
            0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
            100% { transform: perspective(500px) rotateX(60deg) translateY(60px); }
        }
        
        /* Gradient overlays */
        .gradient-overlay {
            position: fixed;
            inset: 0;
            background: 
                radial-gradient(ellipse at 50% 0%, rgba(255, 45, 85, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 0% 100%, rgba(255, 215, 0, 0.1) 0%, transparent 40%),
                radial-gradient(ellipse at 100% 100%, rgba(0, 240, 255, 0.08) 0%, transparent 40%);
            z-index: 1;
            pointer-events: none;
        }
        
        /* Scan line effect */
        .scanlines {
            position: fixed;
            inset: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0,0,0,0.1) 2px,
                rgba(0,0,0,0.1) 4px
            );
            pointer-events: none;
            z-index: 100;
            opacity: 0.3;
        }
        
        /* Floating geometric shapes */
        .shape {
            position: fixed;
            border: 1px solid;
            opacity: 0.15;
            animation: shape-float 15s ease-in-out infinite;
        }
        
        .shape-1 {
            width: 200px; height: 200px;
            border-color: var(--neon-gold);
            top: 10%; right: 15%;
            transform: rotate(45deg);
            animation-delay: 0s;
        }
        
        .shape-2 {
            width: 100px; height: 100px;
            border-color: var(--neon-red);
            bottom: 20%; left: 10%;
            border-radius: 50%;
            animation-delay: -5s;
        }
        
        .shape-3 {
            width: 150px; height: 150px;
            border-color: var(--neon-cyan);
            top: 60%; right: 8%;
            animation-delay: -10s;
        }
        
        @keyframes shape-float {
            0%, 100% { transform: rotate(0deg) scale(1); opacity: 0.15; }
            50% { transform: rotate(180deg) scale(1.1); opacity: 0.25; }
        }
        
        /* Main card */
        .container {
            position: relative;
            z-index: 10;
            width: 90%;
            max-width: 500px;
            animation: card-in 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        @keyframes card-in {
            0% { opacity: 0; transform: translateY(30px) scale(0.95); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        
        .card {
            background: linear-gradient(135deg, rgba(20,20,30,0.9) 0%, rgba(10,10,15,0.95) 100%);
            border: 1px solid rgba(255,215,0,0.2);
            border-radius: 2px;
            padding: 2.5rem;
            position: relative;
            overflow: hidden;
        }
        
        /* Holographic border effect */
        .card::before {
            content: '';
            position: absolute;
            inset: -2px;
            background: linear-gradient(
                90deg,
                var(--neon-gold),
                var(--neon-red),
                var(--neon-cyan),
                var(--neon-gold)
            );
            z-index: -1;
            animation: holo-border 3s linear infinite;
            background-size: 300% 100%;
            opacity: 0.5;
        }
        
        @keyframes holo-border {
            0% { background-position: 0% 50%; }
            100% { background-position: 300% 50%; }
        }
        
        .card::after {
            content: '';
            position: absolute;
            inset: 1px;
            background: linear-gradient(135deg, rgba(20,20,30,0.98) 0%, rgba(10,10,15,1) 100%);
            border-radius: 1px;
            z-index: -1;
        }
        
        /* Corner accents */
        .corner {
            position: absolute;
            width: 20px; height: 20px;
            border-color: var(--neon-gold);
            border-style: solid;
            border-width: 0;
            opacity: 0.6;
        }
        .corner-tl { top: 8px; left: 8px; border-top-width: 2px; border-left-width: 2px; }
        .corner-tr { top: 8px; right: 8px; border-top-width: 2px; border-right-width: 2px; }
        .corner-bl { bottom: 8px; left: 8px; border-bottom-width: 2px; border-left-width: 2px; }
        .corner-br { bottom: 8px; right: 8px; border-bottom-width: 2px; border-right-width: 2px; }
        
        /* Header */
        .header { text-align: center; margin-bottom: 2rem; }
        
        .badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            background: rgba(255,215,0,0.1);
            border: 1px solid rgba(255,215,0,0.3);
            font-size: 0.65rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--neon-gold);
            margin-bottom: 1rem;
        }
        
        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.6rem;
            font-weight: 900;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            background: linear-gradient(135deg, #fff 0%, var(--neon-gold) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.75rem;
        }
        
        .tagline {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.4);
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        
        .hero-text {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.6);
            margin-top: 1.25rem;
            line-height: 1.7;
        }
        
        /* Upload zone */
        .upload-zone {
            position: relative;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 2rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(255,255,255,0.02);
            margin-top: 0.5rem;
        }
        
        .upload-zone:hover {
            border-color: var(--neon-gold);
            background: rgba(255,215,0,0.03);
            box-shadow: 0 0 30px rgba(255,215,0,0.1), inset 0 0 30px rgba(255,215,0,0.02);
        }
        
        .upload-zone.dragover {
            border-color: var(--neon-cyan);
            background: rgba(0,240,255,0.05);
        }
        
        .upload-icon {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            color: var(--neon-gold);
            margin-bottom: 0.75rem;
            opacity: 0.8;
        }
        
        .upload-text {
            font-size: 0.8rem;
            color: rgba(255,255,255,0.5);
        }
        
        .upload-hint {
            font-size: 0.7rem;
            color: rgba(255,255,255,0.25);
            margin-top: 0.5rem;
            font-family: 'IBM Plex Mono', monospace;
        }
        
        input[type="file"] { display: none; }
        
        .file-name {
            margin-top: 1rem;
            padding: 0.6rem 1rem;
            background: rgba(255,215,0,0.08);
            border-left: 2px solid var(--neon-gold);
            font-size: 0.75rem;
            color: var(--neon-gold);
            text-align: left;
            display: none;
        }
        
        .file-name.visible { display: block; }
        
        /* Button */
        .btn-wrap { margin-top: 1.5rem; }
        
        .btn {
            width: 100%;
            padding: 1rem;
            background: transparent;
            color: var(--neon-gold);
            border: 1px solid var(--neon-gold);
            font-family: 'Orbitron', sans-serif;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,215,0,0.2), transparent);
            transition: left 0.5s ease;
        }
        
        .btn:hover::before { left: 100%; }
        
        .btn:hover {
            background: rgba(255,215,0,0.1);
            box-shadow: 0 0 30px rgba(255,215,0,0.3), inset 0 0 20px rgba(255,215,0,0.1);
            text-shadow: 0 0 10px var(--neon-gold);
        }
        
        .btn:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }
        
        .btn:disabled:hover {
            background: transparent;
            box-shadow: none;
            text-shadow: none;
        }
        
        .btn:disabled:hover::before { left: -100%; }
        
        /* Status */
        #status {
            margin-top: 1rem;
            padding: 0.75rem;
            font-size: 0.75rem;
            display: none;
            animation: fade-in 0.3s ease;
        }
        
        @keyframes fade-in {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        
        #status.loading {
            display: block;
            color: var(--neon-gold);
            border-left: 2px solid var(--neon-gold);
            background: rgba(255,215,0,0.05);
        }
        
        #status.success {
            display: block;
            color: var(--neon-cyan);
            border-left: 2px solid var(--neon-cyan);
            background: rgba(0,240,255,0.05);
        }
        
        .spinner {
            display: inline-block;
            width: 12px; height: 12px;
            border: 2px solid rgba(255,215,0,0.2);
            border-top-color: var(--neon-gold);
            border-radius: 50%;
            animation: spin 0.6s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* Footer */
        .footer {
            margin-top: 1.5rem;
            text-align: center;
            font-size: 0.65rem;
            color: rgba(255,255,255,0.2);
            letter-spacing: 0.05em;
        }
        
        /* Glitch effect on hover */
        .container:hover h1 {
            animation: glitch 0.3s ease;
        }
        
        @keyframes glitch {
            0%, 100% { transform: translate(0); }
            20% { transform: translate(-2px, 1px); }
            40% { transform: translate(2px, -1px); }
            60% { transform: translate(-1px, -1px); }
            80% { transform: translate(1px, 1px); }
        }
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="gradient-overlay"></div>
    <div class="scanlines"></div>
    
    <div class="shape shape-1"></div>
    <div class="shape shape-2"></div>
    <div class="shape shape-3"></div>
    
    <div class="container">
        <div class="card">
            <div class="corner corner-tl"></div>
            <div class="corner corner-tr"></div>
            <div class="corner corner-bl"></div>
            <div class="corner corner-br"></div>
            
            <div class="header">
                <div class="badge">◆ Holiday Edition</div>
                <h1>Riddle Workshop</h1>
                <p class="tagline">Bulk Gift Cards • Personalized in Seconds</p>
                <p class="hero-text">Upload your gift list. Download personalized riddle cards for everyone—no spoilers, just clever hints.</p>
            </div>
            
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-zone" id="dropZone">
                    <div class="upload-icon">[ ↑ ]</div>
                    <p class="upload-text">Drop your gift list here</p>
                    <p class="upload-hint">CSV: Name, Gift Idea, Budget</p>
                    <div class="file-name" id="fileName"></div>
                    <input type="file" id="fileInput" name="file" accept=".csv" required>
            </div>
            
            <div class="btn-wrap">
                <button type="submit" class="btn" id="submitBtn" disabled>
                    ► Initialize Generation
                </button>
            </div>
        </form>
        
        <div id="status"></div>
        
        <p class="footer">For teachers • Event planners • Gift enthusiasts</p>
        </div>
    </div>
    
    <script>
        // Upload logic
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
        
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
        
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
                fileName.textContent = fileInput.files[0].name;
                fileName.classList.add('visible');
                submitBtn.disabled = false;
            }
        }
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            submitBtn.disabled = true;
            status.className = 'loading';
            status.innerHTML = '<span class="spinner"></span> Generating riddles...';
            
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
                    status.innerHTML = '✓ Riddles ready — check your downloads';
                } else {
                    throw new Error('Generation failed');
                }
            } catch (error) {
                status.className = 'loading';
                status.innerHTML = '✕ Error: ' + error.message;
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
