import yt_dlp
import os
import shutil
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

console = Console()

class MaldixDownloader:
    def __init__(self):
        self.output_dir = "Maldix_Downloads"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.success_count = 0

    def check_dependencies(self):
        """Verify FFmpeg is installed and accessible."""
        if not shutil.which("ffmpeg"):
            console.print("[bold red]ERROR:[/bold red] FFmpeg not found in System PATH.")
            console.print("Please install it: [cyan]winget install ffmpeg[/cyan]")
            return False
        return True

    def progress_hook(self, d, progress, task_id):
        if d['status'] == 'downloading':
            p = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total > 0:
                progress.update(task_id, completed=p, total=total, description=f"[blue]Downloading: [white]{d['filename'].split(os.sep)[-1][:30]}...")
        elif d['status'] == 'finished':
            self.success_count += 1

    def run(self, url):
        console.clear()
        console.print(Panel.fit("[bold cyan]Maldix YouTube Downloader[/bold cyan]\n[white]GitHub Edition | MP4 | Auto-Skip[/white]", border_style="blue"))
        
        if not self.check_dependencies():
            sys.exit(1)

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'{self.output_dir}/%(uploader)s/%(title)s.%(ext)s',
            'noplaylist': False,
            'ignoreerrors': True,
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [lambda d: self.progress_hook(d, progress, task_id)],
        }

        with Progress(
            TextColumn("{task.description}"),
            BarColumn(bar_width=40),
            "[progress.percentage]{task.percentage:>3.0f}%",
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            
            task_id = progress.add_task("[yellow]Initializing...", total=None)

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                console.print(f"\n[bold red]CRITICAL ERROR:[/bold red] {str(e)}")

        self.show_summary()

    def show_summary(self):
        table = Table(title="Maldix Session Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("Files Saved", str(self.success_count))
        table.add_row("Directory", self.output_dir)
        
        console.print("\n")
        console.print(table)
        console.print("[bold green]Process Complete.[/bold green]")

if __name__ == "__main__":
    app = MaldixDownloader()
    try:
        target = console.input("[bold yellow]Paste URL: [/bold yellow]")
        if target.strip():
            app.run(target)
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted by user. Exiting...[/red]")