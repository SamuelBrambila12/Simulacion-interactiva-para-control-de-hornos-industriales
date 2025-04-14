from browser import document, window, timer
import random, datetime

# Definición de Estados
state_names = {
    "A": "Apagado",
    "I": "Inicialización",
    "MS": "Modo sin seleccionar",
    "REG": "Regular",
    "CON": "Convección",
    "GRI": "Grill",
    "DEF": "Descongelar",
    "T": "Temperatura configurada",
    "TI": "Tiempo configurado",
    "P": "Precalentamiento",
    "E": "Estabilización",
    "C": "Cocción",
    "V": "Verificación",
    "EN": "Enfriamiento",
    "F": "Finalización",
    "ME": "Manejo de errores"
}

# Definimos las listas de estados y eventos en orden
states = ["A", "I", "MS", "REG", "CON", "GRI", "DEF", "T", "TI", "P", "E", "C", "V", "EN", "F", "ME"]
events = ["IN", "SO", "ER", "MSR", "MSC", "MSG", "MSD", "SET-T", "SET-TI", "CONF", "TR", "ST", "TC", "AN", "OK", "CE", "CO", "R"]

# Matriz de transiciones (función f: estado siguiente)
transition_matrix = [
    # IN   SO   ER   MSR  MSC  MSG  MSD  SET-T SET-TI CONF TR   ST   TC   AN   OK   CE   CO   R
    ["I", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],  # A
    ["I", "MS", "ME", "I", "I", "I", "I", "I", "I", "I", "I", "I", "I", "ME", "I", "I", "I", "I"],  # I
    ["MS", "MS", "ME", "REG", "CON", "GRI", "DEF", "MS", "MS", "MS", "MS", "MS", "MS", "ME", "MS", "MS", "MS", "I"],  # MS
    ["REG", "REG", "ME", "REG", "REG", "REG", "REG", "T", "REG", "REG", "REG", "REG", "REG", "ME", "REG", "REG", "REG", "I"],  # REG
    ["CON", "CON", "ME", "CON", "CON", "CON", "CON", "T", "CON", "CON", "CON", "CON", "CON", "ME", "CON", "CON", "CON", "I"],  # CON
    ["GRI", "GRI", "ME", "GRI", "GRI", "GRI", "GRI", "T", "GRI", "GRI", "GRI", "GRI", "GRI", "ME", "GRI", "GRI", "GRI", "I"],  # GRI
    ["DEF", "DEF", "ME", "DEF", "DEF", "DEF", "DEF", "T", "DEF", "DEF", "DEF", "DEF", "DEF", "ME", "DEF", "DEF", "DEF", "I"],  # DEF
    ["T", "T", "ME", "T", "T", "T", "T", "T", "TI", "T", "T", "T", "T", "ME", "T", "T", "T", "I"],  # T
    ["TI", "TI", "ME", "TI", "TI", "TI", "TI", "TI", "TI", "P", "TI", "TI", "TI", "ME", "TI", "TI", "TI", "I"],  # TI
    ["P", "P", "ME", "P", "P", "P", "P", "P", "P", "P", "E", "P", "P", "ME", "P", "P", "P", "I"],  # P
    ["E", "E", "ME", "E", "E", "E", "E", "E", "E", "E", "E", "C", "E", "ME", "E", "E", "E", "I"],  # E
    ["C", "C", "ME", "C", "C", "C", "C", "C", "C", "C", "C", "C", "V", "ME", "C", "C", "C", "I"],  # C
    ["V", "V", "ME", "V", "V", "V", "V", "V", "V", "V", "V", "V", "V", "ME", "EN", "V", "V", "I"],  # V
    ["EN", "EN", "ME", "EN", "EN", "EN", "EN", "EN", "EN", "EN", "EN", "EN", "EN", "ME", "EN", "F", "EN", "I"],  # EN
    ["F", "F", "ME", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "ME", "F", "F", "A", "A"],  # F
    ["ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "ME", "I"]   # ME
]

# Matriz de salidas (función g: símbolo de salida)
output_matrix = [
    # IN   SO   ER   MSR  MSC  MSG  MSD  SET-T SET-TI CONF TR   ST   TC   AN   OK   CE   CO   R
    ["O2", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1", "O1"],  # A
    ["O2", "O3", "O16", "O2", "O2", "O2", "O2", "O2", "O2", "O2", "O2", "O2", "O2", "O16", "O2", "O2", "O2", "O2"],  # I
    ["O3", "O3", "O16", "O4", "O5", "O6", "O7", "O3", "O3", "O3", "O3", "O3", "O3", "O16", "O3", "O3", "O3", "O2"],  # MS
    ["O4", "O4", "O16", "O4", "O4", "O4", "O4", "O8", "O4", "O4", "O4", "O4", "O4", "O16", "O4", "O4", "O4", "O2"],  # REG
    ["O5", "O5", "O16", "O5", "O5", "O5", "O5", "O8", "O5", "O5", "O5", "O5", "O5", "O16", "O5", "O5", "O5", "O2"],  # CON
    ["O6", "O6", "O16", "O6", "O6", "O6", "O6", "O8", "O6", "O6", "O6", "O6", "O6", "O16", "O6", "O6", "O6", "O2"],  # GRI
    ["O7", "O7", "O16", "O7", "O7", "O7", "O7", "O8", "O7", "O7", "O7", "O7", "O7", "O16", "O7", "O7", "O7", "O2"],  # DEF
    ["O8", "O8", "O16", "O8", "O8", "O8", "O8", "O8", "O9", "O8", "O8", "O8", "O8", "O16", "O8", "O8", "O8", "O2"],  # T
    ["O9", "O9", "O16", "O9", "O9", "O9", "O9", "O9", "O9", "O10", "O9", "O9", "O9", "O16", "O9", "O9", "O9", "O2"],  # TI
    ["O10", "O10", "O16", "O10", "O10", "O10", "O10", "O10", "O10", "O10", "O11", "O10", "O10", "O16", "O10", "O10", "O10", "O2"],  # P
    ["O11", "O11", "O16", "O11", "O11", "O11", "O11", "O11", "O11", "O11", "O11", "O12", "O11", "O16", "O11", "O11", "O11", "O2"],  # E
    ["O12", "O12", "O16", "O12", "O12", "O12", "O12", "O12", "O12", "O12", "O12", "O12", "O13", "O16", "O12", "O12", "O12", "O2"],  # C
    ["O13", "O13", "O16", "O13", "O13", "O13", "O13", "O13", "O13", "O13", "O13", "O13", "O13", "O16", "O14", "O13", "O13", "O2"],  # V
    ["O14", "O14", "O16", "O14", "O14", "O14", "O14", "O14", "O14", "O14", "O14", "O14", "O14", "O16", "O14", "O15", "O14", "O14"],  # EN
    ["O15", "O15", "O16", "O15", "O15", "O15", "O15", "O15", "O15", "O15", "O15", "O15", "O15", "O16", "O15", "O15", "O1", "O1"],  # F
    ["O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O16", "O2"]   # ME
]

# Función para obtener el estado siguiente desde la matriz
def next_state(current, event):
    try:
        state_index = states.index(current)
        event_index = events.index(event)
        return transition_matrix[state_index][event_index]
    except ValueError:
        # Si no encuentra el estado o evento, regresa el estado actual
        return current

# Función para obtener la salida desde la matriz
def get_output(state):
    try:
        state_index = states.index(state)
        # Usamos el primer evento como referencia ya que la salida solo depende del estado
        # Podríamos usar cualquier columna, pero elegimos la primera (IN) para simplificar
        return output_matrix[state_index][0]
    except ValueError:
        return "O1"  # Valor por defecto si no encuentra el estado

output_meanings = {
    "O1": "Sistema apagado.",
    "O2": "Iniciado: verifica sensores y protocolos de seguridad.",
    "O3": "Modo sin seleccionar.",
    "O4": "Modo Regular seleccionado.",
    "O5": "Modo Convección seleccionado.",
    "O6": "Modo Grill seleccionado.",
    "O7": "Modo Descongelar seleccionado.",
    "O8": "Temperatura configurada por usuario.",
    "O9": "Tiempo configurado por usuario.",
    "O10": "Inicio de Precalentamiento.",
    "O11": "En proceso de estabilización.",
    "O12": "Cocinando.",
    "O13": "Para verificación.",
    "O14": "Enfriando.",
    "O15": "Finalizado.",
    "O16": "Manejo de errores."
}

default_cooking_times = {
    "regular": 30,
    "convection": 20,
    "grill": 15,
    "defrost": 45
}

current_state = "A"
current_temp = 0
target_temp = 0
cooking_time_minutes = 0
cooking_time_seconds = 0
remaining_time_minutes = 0
remaining_time_seconds = 0
timer_running = False
timer_id = None
global_audio = None

# Elementos de la interfaz
btn_power = document["btn-power"]
btn_reset = document["btn-reset"]
btn_sensors = document["btn-sensors"]
btn_select_mode = document["btn-select-mode"]
cooking_mode = document["cooking-mode"]
temp_up = document["temp-up"]
temp_down = document["temp-down"]
digital_temp_display = document["digital-temp-display"]
btn_temp_reached = document["btn-temp-reached"]
btn_stabilized = document["btn-stabilized"]
btn_time_complete = document["btn-time-complete"]
btn_verification_ok = document["btn-verification-ok"]
btn_cool_enough = document["btn-cool-enough"]
btn_complete = document["btn-complete"]
btn_error = document["btn-error"]
btn_anomaly = document["btn-anomaly"]
temp_display = document["temp-display"]
current_state_elem = document["current-state"]
current_output_elem = document["current-output"]
event_log = document["event-log"]
time_up = document["time-up"]
time_down = document["time-down"]
digital_time_display = document["digital-time-display"]
time_remaining_display = document["time-remaining-display"]

# Elementos del horno
heating_elements = document.select(".heating-element")
oven_contents = document.select_one(".oven-contents")

# Botones de alternancia de vistas
btn_interactive = document["btn-interactive"]
btn_tables = document["btn-tables"]
control_interactive = document["control-interactive"]
transition_tables = document["transition-tables"]

def format_time(minutes, seconds):
    return f"{minutes:02d}:{seconds:02d}"

def play_alert():
    global global_audio
    if current_state == "EN":
        return
    if not global_audio:
        global_audio = window.Audio.new('https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg')
        global_audio.loop = False
    global_audio.play()
    oven_contents.classList.add("complete")
    document.select_one("#oven-display").classList.add("alert")

def stop_alert():
    global global_audio
    if global_audio:
        global_audio.pause()
        global_audio.currentTime = 0

def update_button_state(button, state):
    if state:
        button.style.opacity = "1"
        button.style.cursor = "pointer"
        button.style.backgroundColor = ""
    else:
        button.style.opacity = "0.5"
        button.style.cursor = "not-allowed"
        button.style.backgroundColor = "#999"

def update_interface():
    current_state_elem.text = f"{state_names[current_state]} ({current_state})"
    current_output = get_output(current_state)
    current_output_elem.text = f"{current_output} - {output_meanings[current_output]}"
    
    # Desactivar todos los controles primero
    for btn in [btn_power, btn_reset, btn_sensors, btn_select_mode,
                btn_temp_reached, btn_stabilized, btn_time_complete,
                btn_verification_ok, btn_cool_enough, btn_complete,
                btn_error, btn_anomaly, temp_up, temp_down, time_up, time_down,
                document["btn-set-time"], document["btn-confirm-time"]]:
        update_button_state(btn, False)
    
    # Bloquear selector por defecto
    cooking_mode.disabled = True
    
    digital_temp_display.text = f"{target_temp}°C"
    digital_time_display.text = format_time(cooking_time_minutes, cooking_time_seconds)
    
    if current_state == "C" and timer_running:
        time_remaining_display.text = f"Tiempo restante: {format_time(remaining_time_minutes, remaining_time_seconds)}"
    else:
        time_remaining_display.text = ""
    # Actualizar texto del botón de temperatura
    if current_state in ["A", "REG", "CON", "GRI", "DEF"]:
        btn_temp_reached.text = "Establecer Temperatura (SET-T)"
    elif current_state == "P":
        btn_temp_reached.text = "Temperatura Alcanzada (TR)"
    # Habilitar controles según el estado
    if current_state == "A":
        update_button_state(btn_power, True)
        update_button_state(btn_error, True)
    elif current_state == "I":
        update_button_state(btn_sensors, True)
        update_button_state(btn_error, True)
    elif current_state == "MS":
        cooking_mode.disabled = False
        update_button_state(btn_select_mode, True)
        update_button_state(temp_up, True)
        update_button_state(temp_down, True)
        update_button_state(time_up, True)
        update_button_state(time_down, True)
        update_button_state(btn_error, True)
    elif current_state in ["REG", "CON", "GRI", "DEF"]:
        update_button_state(temp_up, True)
        update_button_state(temp_down, True)
        update_button_state(btn_temp_reached, True)
        update_button_state(btn_error, True)
    elif current_state == "T":
        update_button_state(time_up, True)
        update_button_state(time_down, True)
        update_button_state(document["btn-set-time"], True)
        update_button_state(btn_error, True)
    elif current_state == "TI":
        update_button_state(document["btn-confirm-time"], True)
        update_button_state(btn_error, True)
    elif current_state == "P":
        update_button_state(btn_temp_reached, True)  # Para disparar "TR"
        update_button_state(btn_error, True)
    elif current_state == "E":
        update_button_state(btn_stabilized, True)
        update_button_state(btn_error, True)
    elif current_state == "C":
        update_button_state(btn_time_complete, True)
        update_button_state(btn_anomaly, True)
    elif current_state == "V":
        update_button_state(btn_verification_ok, True)
        update_button_state(btn_error, True)
    elif current_state == "EN":
        update_button_state(btn_cool_enough, True)
        update_button_state(btn_error, True)
    elif current_state == "F":
        update_button_state(btn_complete, True)
    elif current_state == "ME":
        update_button_state(btn_reset, True)
    
    update_oven_visualization()

def update_oven_visualization():
    for element in heating_elements:
        element.classList.remove("active")
    oven_contents.classList.remove("cooking")
    
    if current_state == "P":
        for element in heating_elements:
            element.classList.add("active")
    elif current_state == "E":
        heating_elements[0].classList.add("active")
    elif current_state == "C":
        heating_elements[0].classList.add("active")
        oven_contents.classList.add("cooking")
    elif current_state == "V":
        oven_contents.classList.add("cooking")
    elif current_state == "EN":
        oven_contents.classList.remove("complete")
        document.select_one("#oven-display").classList.remove("alert")
        stop_alert()
    elif current_state == "ME":
        for element in heating_elements:
            element.classList.add("active")
        timer.set_timeout(lambda: [element.classList.remove("active") for element in heating_elements], 500)
        timer.set_timeout(lambda: [element.classList.add("active") for element in heating_elements], 1000)

def log_event(event_type, message, event_class=""):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = document.createElement("div")
    log_entry.classList.add("log-entry")
    log_entry.innerHTML = f"""
      <span class="log-time">[{current_time}]</span>
      <span class="log-event {event_class}">{event_type}:</span>
      {message}
    """
    event_log.insertBefore(log_entry, event_log.firstChild)

def simulate_temperature():
    global current_temp
    if current_state == "P":
        if current_temp < target_temp:
            current_temp += random.randint(5, 15)
            if current_temp > target_temp:
                current_temp = target_temp
    elif current_state == "E":
        current_temp += random.randint(-3, 3)
        if current_temp > target_temp + 5:
            current_temp = target_temp + 5
        elif current_temp < target_temp - 5:
            current_temp = target_temp - 5
    elif current_state == "C":
        current_temp += random.randint(-1, 1)
    elif current_state == "EN":
        if current_temp > 50:
            current_temp -= random.randint(5, 10)
        else:
            current_temp -= random.randint(1, 3)
        if current_temp < 0:
            current_temp = 0
    elif current_state == "A":
        if current_temp > 0:
            current_temp -= random.randint(1, 5)
        if current_temp < 0:
            current_temp = 0
    temp_display.text = f"{current_temp}°C"
    if current_state not in ["A", "I", "MS", "F", "ME"]:
        timer.set_timeout(simulate_temperature, 1000)

def update_timer():
    global remaining_time_minutes, remaining_time_seconds, timer_running
    if remaining_time_minutes == 0 and remaining_time_seconds == 0:
        timer_running = False
        if current_state == "C":
            log_event("INFO", "Tiempo de cocción completado automáticamente")
            play_alert() 
            handle_transition("TC")
        return
    if remaining_time_seconds == 0:
        remaining_time_minutes -= 1
        remaining_time_seconds = 59
    else:
        remaining_time_seconds -= 1
    time_remaining_display.text = f"Tiempo restante: {format_time(remaining_time_minutes, remaining_time_seconds)}"
    if timer_running:
        global timer_id
        timer_id = timer.set_timeout(update_timer, 1000)

def start_cooking_timer():
    global remaining_time_minutes, remaining_time_seconds, timer_running
    remaining_time_minutes = cooking_time_minutes
    remaining_time_seconds = cooking_time_seconds
    timer_running = True
    update_timer()

def handle_transition(event_type):
    global current_state, timer_running
    new_state = next_state(current_state, event_type)
    if new_state == current_state and event_type not in ["IN", "ER", "R"]:
        log_event("INFO", f"El evento {event_type} no tiene efecto en el estado {current_state}")
        return
    old_state = current_state
    current_state = new_state
    
    # Obtener output usando la matriz de salidas y el estado actual
    state_index = states.index(current_state)
    event_index = events.index(event_type)
    output_code = output_matrix[state_index][event_index]
    
    if old_state != "C" and current_state == "C":
        start_cooking_timer()
    elif old_state == "C" and current_state != "C":
        timer_running = False
    update_interface()
    event_class = ""
    if event_type in ["ER", "AN"]:
        event_class = "error"
    elif event_type in ["OK", "CO"]:
        event_class = "success"
    log_event(event_type, f"Transición: {state_names[old_state]} → {state_names[current_state]}. Salida: {output_code} - {output_meanings[output_code]}", event_class)
    if old_state != "T" and current_state == "T":
        simulate_temperature()

def check_and_handle(event, event_type):
    button = event.currentTarget
    if button.style.opacity != "0.5":
        handle_transition(event_type)

# Ajuste del botón de Temperatura Alcanzada:
def on_temp_reached_click(event):
    if current_state in ["REG", "CON", "GRI", "DEF"]:
        check_and_handle(event, "SET-T")
    elif current_state == "P":
        check_and_handle(event, "TR")

def on_set_time_click(event): check_and_handle(event, "SET-TI")
def on_confirm_time_click(event): check_and_handle(event, "CONF")
def on_power_click(event): check_and_handle(event, "IN")
def on_reset_click(event): check_and_handle(event, "R")
def on_sensors_click(event): check_and_handle(event, "SO")
def on_select_mode_click(event):
    global cooking_time_minutes, cooking_time_seconds
    mode = cooking_mode.value
    if mode == "none":
        log_event("ERROR", "Debe seleccionar un modo de cocción", "error")
        return
    if mode == "regular":
        check_and_handle(event, "MSR")
    elif mode == "convection":
        check_and_handle(event, "MSC")
    elif mode == "grill":
        check_and_handle(event, "MSG")
    elif mode == "defrost":
        check_and_handle(event, "MSD")
def on_temp_up_click(event):
    global target_temp
    if target_temp < 300:
        target_temp += 5
        digital_temp_display.text = f"{target_temp}°C"
        log_event("INFO", f"Temperatura objetivo ajustada a: {target_temp}°C")
def on_temp_down_click(event):
    global target_temp
    if target_temp > 0:
        target_temp -= 5
        digital_temp_display.text = f"{target_temp}°C"
        log_event("INFO", f"Temperatura objetivo ajustada a: {target_temp}°C")
def on_time_up_click(event):
    global cooking_time_minutes, cooking_time_seconds
    if cooking_time_minutes < 99:
        cooking_time_minutes += 1
        digital_time_display.text = format_time(cooking_time_minutes, cooking_time_seconds)
        log_event("INFO", f"Tiempo de cocción ajustado a: {format_time(cooking_time_minutes, cooking_time_seconds)}")
def on_time_down_click(event):
    global cooking_time_minutes, cooking_time_seconds
    if cooking_time_minutes > 0:
        cooking_time_minutes -= 1
        digital_time_display.text = format_time(cooking_time_minutes, cooking_time_seconds)
        log_event("INFO", f"Tiempo de cocción ajustado a: {format_time(cooking_time_minutes, cooking_time_seconds)}")
def on_stabilized_click(event): check_and_handle(event, "ST")
def on_time_complete_click(event): check_and_handle(event, "TC")
def on_verification_ok_click(event): check_and_handle(event, "OK")
def on_cool_enough_click(event): check_and_handle(event, "CE")
def on_complete_click(event): check_and_handle(event, "CO")
def on_error_click(event): check_and_handle(event, "ER")
def on_anomaly_click(event): check_and_handle(event, "AN")

btn_power.bind("click", on_power_click)
btn_reset.bind("click", on_reset_click)
btn_sensors.bind("click", on_sensors_click)
btn_select_mode.bind("click", on_select_mode_click)
temp_up.bind("click", on_temp_up_click)
temp_down.bind("click", on_temp_down_click)
time_up.bind("click", on_time_up_click)
time_down.bind("click", on_time_down_click)
btn_temp_reached.bind("click", on_temp_reached_click)
document["btn-set-time"].bind("click", on_set_time_click)
document["btn-confirm-time"].bind("click", on_confirm_time_click)
btn_stabilized.bind("click", on_stabilized_click)
btn_time_complete.bind("click", on_time_complete_click)
btn_verification_ok.bind("click", on_verification_ok_click)
btn_cool_enough.bind("click", on_cool_enough_click)
btn_complete.bind("click", on_complete_click)
btn_error.bind("click", on_error_click)
btn_anomaly.bind("click", on_anomaly_click)

# Funciones para alternar vistas (toggle)
def show_interactive(event):
    control_interactive.style.display = "block"
    transition_tables.style.display = "none"
    btn_interactive.classList.add("active")
    btn_tables.classList.remove("active")

def show_tables(event):
    control_interactive.style.display = "none"
    transition_tables.style.display = "block"
    btn_tables.classList.add("active")
    btn_interactive.classList.remove("active")

btn_interactive.bind("click", show_interactive)
btn_tables.bind("click", show_tables)

update_interface()
log_event("SISTEMA", "Simulador de Hornos Industriales inicializado")