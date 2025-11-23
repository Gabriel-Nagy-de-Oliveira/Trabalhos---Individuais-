import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_abline, ggsave


# ----------------------------------------------
# 1. Ler os dados X e y a partir dos arquivos .txt
# ----------------------------------------------
X = np.loadtxt("X.txt")   # anos de estudo
y = np.loadtxt("y.txt")   # salário

# Garantir que X seja vetor coluna
X = X.reshape(-1, 1)

# ----------------------------------------------
# 2. Calcular os coeficientes pela fórmula matricial
# ----------------------------------------------
# Criar matriz com coluna de 1s (intercepto)
ones = np.ones((X.shape[0], 1))
X_design = np.hstack((ones, X))

# β = (X'X)^(-1) X'y
beta = np.linalg.inv(X_design.T @ X_design) @ (X_design.T @ y)

a = beta[0]   # intercepto
b = beta[1]   # inclinação

print("Coeficientes calculados:")
print("Intercepto (a):", a)
print("Inclinação (b):", b)

# ----------------------------------------------
# 3. Criar o gráfico no formato EXIGIDO
# ----------------------------------------------
df = {"x": X.flatten(), "y": y}

plot = (
    ggplot(pd.DataFrame(df), aes("x", "y"))
    + geom_point()
    + geom_abline(intercept=a, slope=b)
)

plot.save("grafico.png")   # <<< funciona no Python 3.12

