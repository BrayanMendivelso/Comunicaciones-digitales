% Comunicaciones Digitales UMNG / jose.rugeles@Unimilitar.edu.co
% Programa: muestreo

f = 625;        % frecuencia de la señal (Hz)
T = 1/f;        % periodo (s)
A = 1.6;        % amplitud (V)
NT = 2;         % nº de periodos a capturar
N = 40;         % nº de muestras por periodo
ts = T/N;       % periodo de muestreo (s)

% Vector de tiempo para las muestras (N*NT puntos exactos)
t = 0:ts:(NT*T - ts);
V = A * sin(2*pi*f*t);  % señal muestreada

% Señal continua para comparación
t_cont = 0:ts/20:NT*T;
V_cont = A * sin(2*pi*f*t_cont);

% ===== Gráfica =====
figure('Position',[100 100 900 400]);  % tamaño ventana
plot(t_cont, V_cont, 'b-', 'LineWidth',2); hold on;
stem(t, V, 'r','filled','LineWidth',1.5);

xlabel('Tiempo (s)','FontSize',20,'FontWeight','bold');
ylabel('Amplitud (V)','FontSize',20,'FontWeight','bold');
title(sprintf('Muestreo de un seno f=%d Hz, N=%d muestras/periodo', f, N), ...
      'FontSize',20,'FontWeight','bold');

legend({'Señal continua','Muestras'},'FontSize',14,'Location','best');
grid on;
set(gca,'FontSize',16,'LineWidth',1.2);   
