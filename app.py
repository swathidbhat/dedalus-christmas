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
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --gold: #d4af37;
            --gold-light: #f4e4bc;
            --crimson: #8b0000;
            --deep: #0a0a0f;
            --card-bg: rgba(20, 20, 30, 0.6);
        }
        
        body {
            min-height: 100vh;
            font-family: 'Syne', sans-serif;
            background: var(--deep);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            perspective: 1000px;
            overflow: hidden;
        }
        
        /* Animated gradient background */
        .bg-gradient {
            position: fixed;
            inset: 0;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(139, 0, 0, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(20, 20, 40, 1) 0%, var(--deep) 100%);
            z-index: 0;
        }
        
        /* 3D Floating orbs */
        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(1px);
            animation: float 20s ease-in-out infinite;
            z-index: 1;
        }
        
        .orb-1 {
            width: 300px; height: 300px;
            background: radial-gradient(circle at 30% 30%, rgba(212, 175, 55, 0.3), transparent 70%);
            top: -100px; right: -50px;
            animation-delay: 0s;
        }
        
        .orb-2 {
            width: 200px; height: 200px;
            background: radial-gradient(circle at 30% 30%, rgba(139, 0, 0, 0.4), transparent 70%);
            bottom: -50px; left: -50px;
            animation-delay: -7s;
        }
        
        .orb-3 {
            width: 150px; height: 150px;
            background: radial-gradient(circle at 30% 30%, rgba(212, 175, 55, 0.2), transparent 70%);
            top: 50%; left: 10%;
            animation-delay: -14s;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) rotate(0deg) scale(1); }
            25% { transform: translate(30px, -30px) rotate(5deg) scale(1.05); }
            50% { transform: translate(-20px, 20px) rotate(-5deg) scale(0.95); }
            75% { transform: translate(20px, 10px) rotate(3deg) scale(1.02); }
        }
        
        /* Particle field */
        .particles {
            position: fixed;
            inset: 0;
            z-index: 1;
            pointer-events: none;
        }
        
        .particle {
            position: absolute;
            width: 3px; height: 3px;
            background: var(--gold);
            border-radius: 50%;
            opacity: 0;
            animation: particle-fall linear infinite;
        }
        
        @keyframes particle-fall {
            0% { opacity: 0; transform: translateY(-10vh) translateX(0) scale(0); }
            10% { opacity: 1; transform: scale(1); }
            90% { opacity: 0.5; }
            100% { opacity: 0; transform: translateY(110vh) translateX(20px) scale(0.5); }
        }
        
        /* Main container with 3D effect */
        .container {
            position: relative;
            z-index: 10;
            width: 90%;
            max-width: 520px;
            padding: 3rem;
            background: var(--card-bg);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 24px;
            backdrop-filter: blur(20px);
            box-shadow: 
                0 0 0 1px rgba(255,255,255,0.05) inset,
                0 50px 100px -20px rgba(0,0,0,0.5),
                0 0 60px rgba(212, 175, 55, 0.1);
            transform-style: preserve-3d;
            animation: card-entrance 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        @keyframes card-entrance {
            0% { opacity: 0; transform: translateY(40px) rotateX(10deg); }
            100% { opacity: 1; transform: translateY(0) rotateX(0); }
        }
        
        /* Header */
        .header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .logo {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .logo-icon {
            width: 40px; height: 40px;
            background: linear-gradient(135deg, var(--gold) 0%, var(--crimson) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            animation: icon-glow 3s ease-in-out infinite;
        }
        
        @keyframes icon-glow {
            0%, 100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
            50% { box-shadow: 0 0 40px rgba(212, 175, 55, 0.6); }
        }
        
        h1 {
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #fff 0%, var(--gold-light) 50%, var(--gold) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tagline {
            font-size: 0.85rem;
            color: var(--gold);
            font-weight: 600;
            margin-top: 0.5rem;
            letter-spacing: 0.05em;
        }
        
        .hero-text {
            font-size: 1rem;
            color: rgba(255,255,255,0.7);
            margin-top: 1rem;
            line-height: 1.6;
            font-weight: 400;
        }
        
        /* Upload zone */
        .upload-zone {
            position: relative;
            border: 1px dashed rgba(212, 175, 55, 0.3);
            border-radius: 16px;
            padding: 2.5rem 2rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            background: rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .upload-zone::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, transparent 50%);
            opacity: 0;
            transition: opacity 0.4s;
        }
        
        .upload-zone:hover {
            border-color: var(--gold);
            transform: translateY(-2px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .upload-zone:hover::before { opacity: 1; }
        
        .upload-zone.dragover {
            border-color: var(--gold);
            background: rgba(212, 175, 55, 0.1);
            transform: scale(1.02);
        }
        
        .upload-icon {
            width: 60px; height: 60px;
            margin: 0 auto 1rem;
            border: 2px solid rgba(212, 175, 55, 0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            transition: all 0.4s;
        }
        
        .upload-zone:hover .upload-icon {
            border-color: var(--gold);
            transform: scale(1.1) rotate(5deg);
        }
        
        .upload-text {
            font-size: 0.95rem;
            color: rgba(255,255,255,0.7);
        }
        
        .upload-text span {
            color: var(--gold);
            font-weight: 600;
        }
        
        .upload-hint {
            font-size: 0.8rem;
            color: rgba(255,255,255,0.4);
            margin-top: 0.5rem;
            font-family: 'JetBrains Mono', monospace;
        }
        
        input[type="file"] { display: none; }
        
        .file-name {
            margin-top: 1rem;
            padding: 0.75rem 1rem;
            background: rgba(212, 175, 55, 0.1);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--gold);
            display: none;
        }
        
        .file-name.visible { display: block; }
        
        /* Button */
        .btn-wrap { text-align: center; margin-top: 1.5rem; }
        
        .btn {
            position: relative;
            padding: 1rem 2.5rem;
            background: linear-gradient(135deg, var(--gold) 0%, #b8960b 100%);
            color: var(--deep);
            border: none;
            border-radius: 50px;
            font-family: 'Syne', sans-serif;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
            transform: translateX(-100%);
            transition: transform 0.6s;
        }
        
        .btn:hover::before { transform: translateX(100%); }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(212, 175, 55, 0.4);
        }
        
        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .btn:disabled:hover::before { transform: translateX(-100%); }
        
        /* Status */
        #status {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            font-size: 0.9rem;
            display: none;
            animation: status-in 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        @keyframes status-in {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        #status.loading {
            display: block;
            background: rgba(212, 175, 55, 0.1);
            border: 1px solid rgba(212, 175, 55, 0.2);
            color: var(--gold-light);
        }
        
        #status.success {
            display: block;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #86efac;
        }
        
        .spinner {
            display: inline-block;
            width: 16px; height: 16px;
            border: 2px solid rgba(212, 175, 55, 0.2);
            border-top-color: var(--gold);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* Footer hint */
        .hint {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.3);
            font-family: 'JetBrains Mono', monospace;
        }
        
        .hint code {
            padding: 0.2rem 0.5rem;
            background: rgba(255,255,255,0.05);
            border-radius: 4px;
            color: rgba(255,255,255,0.5);
        }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    
    <div class="particles" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="logo-icon">✦</div>
            </div>
            <h1>The Riddle Workshop</h1>
            <p class="tagline">Bulk Gift Cards, Personalized in Seconds</p>
            <p class="hero-text">Got 50 gifts to wrap? Upload your CSV and download riddle cards for everyone—no spoilers, just hints.</p>
        </div>
        
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-zone" id="dropZone">
                <div class="upload-icon">↑</div>
                <p class="upload-text">Your gift list goes here</p>
                <p class="upload-hint">CSV with Name, Gift Idea, Budget</p>
                <div class="file-name" id="fileName"></div>
                <input type="file" id="fileInput" name="file" accept=".csv" required>
            </div>
            
            <div class="btn-wrap">
                <button type="submit" class="btn" id="submitBtn" disabled>
                    Generate All Riddles
                </button>
            </div>
        </form>
        
        <div id="status"></div>
        
        <p class="hint">Perfect for teachers, event planners, or anyone with a big list</p>
    </div>
    
    <script>
        // Create particles
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 30; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.left = Math.random() * 100 + '%';
            p.style.animationDuration = (8 + Math.random() * 12) + 's';
            p.style.animationDelay = Math.random() * 10 + 's';
            p.style.width = p.style.height = (2 + Math.random() * 3) + 'px';
            particlesContainer.appendChild(p);
        }
        
        // 3D tilt effect on container
        const container = document.querySelector('.container');
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 10;
            const y = (e.clientY / window.innerHeight - 0.5) * 10;
            container.style.transform = `rotateY(${x}deg) rotateX(${-y}deg)`;
        });
        
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
