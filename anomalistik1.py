import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

class AnomalisticDashboard:
    def __init__(self):
        # Initialisiere Daten für die Faltung
        self.steps = 100000
        self.eps = np.linspace(1e-4, 0.2, self.steps)
        
        # Startparameter
        self.init_w0 = 0.5       # Startwert Lügner-Satz
        self.init_freq = 1.0     # Frequenzfaktor für P1/P2
        self.init_dl = 1.5       # Logische Hausdorff-Dimension
        
        # Setup des Plot-Fensters
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(11, 8.5))
        plt.subplots_adjust(bottom=0.35, hspace=0.4) # Platz für interaktive Steuerelemente
        
        self.fig.suptitle("Interaktives Anomalistik-Dashboard (LeviOHsa11;mithilfe von ai erstellt)", fontsize=14, fontweight='bold')
        
        # Zeichne initiale Plots
        self.plot_convolution()
        self.plot_liar_paradox()
        
        # --- Erstellung der interaktiven Widgets ---
        ax_color = 'lightgoldenrodyellow'
        
        # Slider für Lügner-Satz Startwert W(L_0)
        self.ax_w0 = plt.axes([0.15, 0.22, 0.65, 0.03], facecolor=ax_color)
        self.slider_w0 = Slider(self.ax_w0, 'Lügner $W(L_0)$', 0.0, 1.0, valinit=self.init_w0, valstep=0.05)
        
        # Slider für Oszillations-Frequenz
        self.ax_freq = plt.axes([0.15, 0.16, 0.65, 0.03], facecolor=ax_color)
        self.slider_freq = Slider(self.ax_freq, 'Frequenz $P_1/P_2$', 0.1, 5.0, valinit=self.init_freq)
        
        # Slider für Hausdorff-Dimension D_L
        self.ax_dl = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=ax_color)
        self.slider_dl = Slider(self.ax_dl, 'Dimension $D_L$', 1.0, 2.0, valinit=self.init_dl, valstep=0.1)
        
        # Reset-Knopf
        self.ax_reset = plt.axes([0.8, 0.02, 0.1, 0.04])
        self.btn_reset = Button(self.ax_reset, 'Reset', color=ax_color, hovercolor='0.975')
        
        # Event-Verknüpfungen (Zuweisung der Logik bei Änderung)
        self.slider_w0.on_changed(self.update_plots)
        self.slider_freq.on_changed(self.update_plots)
        self.slider_dl.on_changed(self.update_plots)
        self.btn_reset.on_clicked(self.reset_widgets)

    def plot_convolution(self):
        """Berechnet und zeichnet die fraktale Faltung."""
        self.ax1.clear()
        freq = self.init_freq if not hasattr(self, 'slider_freq') else self.slider_freq.val
        
        # Logeme mit dynamischer Frequenz
        w1_imag = 0.5 * np.sin(freq / self.eps)
        w2_imag = -0.5 * np.sin(freq / self.eps)
        
        # Integrand und kumulativer Attraktorverlauf
        integrand = (0.5 + 0.5j * np.sin(freq / self.eps)) * (0.5 - 0.5j * np.sin(freq / self.eps))
        dx = (0.2 - 1e-4) / self.steps
        cumulative_integral = np.cumsum(integrand) * dx
        cumulative_attractor = (cumulative_integral / self.eps) / 0.375
        
        # Plotting
        self.ax1.plot(self.eps, w1_imag, label="Imaginärteil $P_1$ (Oszillation)", color='blue', alpha=0.3, linewidth=0.7)
        self.ax1.plot(self.eps, w2_imag, label="Imaginärteil $P_2$ (Phase)", color='orange', alpha=0.3, linewidth=0.7)
        self.ax1.plot(self.eps, cumulative_attractor.real, label="Attraktor $P_1 \circledast P_2$", color='red', linewidth=2)
        
        self.ax1.set_title("Fraktaler Faltungskalkül & Interferenz (Axiom 3)")
        self.ax1.set_xlabel("Skalierungstiefe ($\epsilon$)")
        self.ax1.set_ylabel("Amplitude")
        self.ax1.set_xlim(0, 0.2)
        self.ax1.set_ylim(-0.6, 1.4)
        self.ax1.grid(True, linestyle='--', alpha=0.5)
        self.ax1.legend(loc="upper right")

    def plot_liar_paradox(self):
        """Berechnet und zeichnet das Lügner-Paradoxon basierend auf Theorem I."""
        self.ax2.clear()
        w0 = self.init_w0 if not hasattr(self, 'slider_w0') else self.slider_w0.val
        dl = self.init_dl if not hasattr(self, 'slider_dl') else self.slider_dl.val
        
        # Iteration der Trajektorie: W(L_n+1) = 1 - W(L_n)
        steps_l = np.arange(0, 12)
        trajectory = [w0]
        for _ in range(11):
            trajectory.append(1.0 - trajectory[-1])
            
        # Plotting der Trajektorie
        self.ax2.step(steps_l, trajectory, where='mid', color='purple', marker='o', linewidth=1.8, label="Wahrheitswert $W(L_n)$")
        
        # Horizontale Linie für die gewählte Hausdorff-Dimension
        self.ax2.axhline(dl, color='darkred', linestyle=':', linewidth=1.5, label=f"Eingestellte Dimension $D_L = {dl:.2f}$")
        
        self.ax2.set_title(f"Theorem I: Lügner-Trajektorie bei Startwert $W(L_0) = {w0}$")
        self.ax2.set_xlabel("Diskrete Zoom-Stufe ($n$)")
        self.ax2.set_ylabel("Logischer Wert")
        self.ax2.set_xticks(steps_l)
        self.ax2.set_ylim(-0.2, 2.2)
        self.ax2.grid(True, linestyle='--', alpha=0.5)
        self.ax2.legend(loc="upper right")

    def update_plots(self, val):
        """Wird aufgerufen, sobald ein Slider bewegt wird."""
        self.plot_convolution()
        self.plot_liar_paradox()
        self.fig.canvas.draw_idle() # Aktualisiert die Ansicht flüssig

    def reset_widgets(self, event):
        """Setzt alle Slider auf die mathematischen Ursprungswerte deines Papers zurück."""
        self.slider_w0.reset()
        self.slider_freq.reset()
        self.slider_dl.reset()

if __name__ == "__main__":
    dashboard = AnomalisticDashboard()
    plt.show()
