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
        # putting stuff here so my desktop isnt a mess
        self.output_dir = "Maldix_Downloads"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.success_count = 0

    def check_dependencies(self):
        # need ffmpeg or the whole thing breaks
        if not shutil.which("ffmpeg"):
            console.print("[bold red]ERROR:[/bold red] you forgot to install ffmpeg.")
            console.print("run this: [cyan]winget install ffmpeg[/cyan] then restart.")
            return False
        return True

    def progress_hook(self, d, progress, task_id):
        # just making sure the bar actually moves
        if d['status'] == 'downloading':
            p = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total > 0:
                progress.update(task_id, completed=p, total=total, description=f"[blue]downloading: [white]{d['filename'].split(os.sep)[-1][:30]}...")
        elif d['status'] == 'finished':
            self.success_count += 1

    def run(self, url):
        console.clear()
        console.print(Panel.fit("[bold cyan]Maldix YouTube Downloader[/bold cyan]\n[white]v1.0.0 | mp4 mode[/white]", border_style="blue"))
        
        if not self.check_dependencies():
            sys.exit(1)

        ydl_opts = {
            # mp4 only because webm is trash
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            # folders named after the channel so it stays organized
            'outtmpl': f'{self.output_dir}/%(uploader)s/%(title)s.%(ext)s',
            'noplaylist': False,
            # skip the dead/private vids so it doesnt crash
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
            
            task_id = progress.add_task("[yellow]thinking...", total=None)

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                console.print(f"\n[bold red]it broke:[/bold red] {str(e)}")

        self.show_summary()

    def show_summary(self):
        # quick look at what happened
        table = Table(title="summary")
        table.add_column("what", style="cyan")
        table.add_column("how many", style="magenta")
        table.add_row("videos saved", str(self.success_count))
        table.add_row("where", self.output_dir)
        
        console.print("\n")
        console.print(table)
        console.print("[bold green]done. go check the folder.[/bold green]")

if __name__ == "__main__":
    app = MaldixDownloader()
    try:
        # paste the link and go
        target = console.input("[bold yellow]paste link: [/bold yellow]")
        if target.strip():
            app.run(target)
    except KeyboardInterrupt:
        # quit nicely if i hit ctrl+c
        console.print("\n[red]closed.[/red]")
