import random
import heapq

# clase para representar un cliente con su tiempo de llegada, inicio de servicio y tiempo de salida
class Customer:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.departure_time = None
# clase para representar un evento en la simulación, como llegada o salida de un cliente
class Event:
    def __init__(self, time, event_type, customer=None):
        self.time = time
        self.event_type = event_type 
        self.customer = customer
    # metodo para comparar eventos por tiempo, necesario para la cola de eventos
    def __lt__(self, other):
        return self.time < other.time
# clase para simular un sistema de colas, donde los clientes llegan y son atendidos por un servidor
class QueueSimulator:
    def __init__(self, arrival_rate, service_rate, simulation_time):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulation_time = simulation_time

        self.clock = 0.0
        self.queue = []
        self.server_busy = False
        self.event_list = []
        self.customers = []
    #metodo para generar el tiempo de llegada de un cliente basado en una distribución exponencial
    def generate_arrival_time(self):
        return random.expovariate(self.arrival_rate)
    # metodo para generar el tiempo de servicio de un cliente basado en una distribución exponencial
    def generate_service_time(self):
        return random.expovariate(self.service_rate)
    # metodo para programar un evento en la lista de eventos, usando una cola de prioridad
    def schedule_event(self, event):
        heapq.heappush(self.event_list, event)
    # metodo para iniciar la simulación, generando el primer evento de llegada
    def run(self):
        arrival_time = self.generate_arrival_time()
        self.schedule_event(Event(arrival_time, 'arrival'))

        while self.event_list and self.clock <= self.simulation_time:
            event = heapq.heappop(self.event_list)
            self.clock = event.time

            if event.event_type == 'arrival':
                self.handle_arrival(event)
            elif event.event_type == 'departure':
                self.handle_departure(event)

        self.report_statistics()
    #metodo para manejar la llegada de un cliente, creando un nuevo cliente y programando su salida si el servidor está ocupado
    def handle_arrival(self, event):
        customer = Customer(self.clock)
        self.customers.append(customer)

        if not self.server_busy:
            self.server_busy = True
            customer.service_start_time = self.clock
            service_time = self.generate_service_time()
            customer.departure_time = self.clock + service_time
            self.schedule_event(Event(customer.departure_time, 'departure', customer))
        else:
            self.queue.append(customer)

        next_arrival = self.clock + self.generate_arrival_time()
        if next_arrival <= self.simulation_time:
            self.schedule_event(Event(next_arrival, 'arrival'))
    # metodo para manejar la salida de un cliente, actualizando el estado del servidor y programando la salida del siguiente cliente en la cola si existe
    def handle_departure(self, event):
        if self.queue:
            customer = self.queue.pop(0)
            customer.service_start_time = self.clock
            service_time = self.generate_service_time()
            customer.departure_time = self.clock + service_time
            self.schedule_event(Event(customer.departure_time, 'departure', customer))
        else:
            self.server_busy = False
    # metodo para reportar estadísticas de la simulación, como el tiempo promedio de espera y el tiempo total en el sistema
    def report_statistics(self):
        wait_times = [
            c.service_start_time - c.arrival_time for c in self.customers if c.service_start_time is not None
        ]
        total_times = [
            c.departure_time - c.arrival_time for c in self.customers if c.departure_time is not None
        ]

        print(f"Total customers served: {len(self.customers)}")
        print(f"Average waiting time in queue: {sum(wait_times)/len(wait_times):.2f}")
        print(f"Average time in system: {sum(total_times)/len(total_times):.2f}")
