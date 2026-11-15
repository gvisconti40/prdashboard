import re

path = r'C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql\app.py'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

funcion_estilo = '''
def aplicar_estilo_farma(fig):
    if fig is None:
        return fig
    fig.update_layout(
        plot_bgcolor="#5a6876",
        paper_bgcolor="#475564",
        font=dict(color="#f1f5f9", family="Inter, sans-serif"),
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="#0d9488",
            font=dict(color="#ffffff", size=13, family="Inter, sans-serif")
        )
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)")
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)")
    return fig
'''

if 'def aplicar_estilo_farma' not in code:
    code = code.replace('pio.templates.default = "farma_center_theme"', 'pio.templates.default = "farma_center_theme"\n' + funcion_estilo)

def replacer(m):
    var_name = m.group(1)
    if 'aplicar_estilo_farma' in var_name:
        return m.group(0)
    return f'st.plotly_chart(aplicar_estilo_farma({var_name})'

code_mod = re.sub(r'st\.plotly_chart\((\w+)', replacer, code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(code_mod)

print("Actualizacion exitosa de todos los graficos.")
