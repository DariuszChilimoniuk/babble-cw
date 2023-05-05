from dataclasses import dataclass


class EventSelector:

    def __init__(self, source_file_path, filter_in=[]) -> None:
        self.source = open(source_file_path, "r")
        self.filter_in = filter_in
        self.current_event = None
        self.current_event = self.read_next_event()
        self.current_time_frame_begin = 0.0
        self.current_time_frame_end = 0.0

    def select_events_in_time_frame(self, time_frame):
        if not self.current_event:
            return None # no more events in the file
        result = list()
        self.current_time_frame_end += time_frame
        while True:
            if self.current_time_frame_begin <= self.event_time() < self.current_time_frame_end:
                if not self.filter_in or self.event_name() in self.filter_in:
                    result.append(self.current_event)
                self.current_event = self.read_next_event()
                if not self.current_event:
                    break # End Of File reached
            else:
                break # not matching event ends building the current result
        self.current_time_frame_begin = self.current_time_frame_end
        return result

    def select(self, time_beg, time_end):
        if not self.current_event:
            return None # no more events in the file
        result = list()
        while True:
            if time_beg <= self.event_time() < time_end:
                if not self.filter_in or self.event_name() in self.filter_in:
                    result.append(self.current_event)
                self.current_event = self.read_next_event()
                if not self.current_event:
                    break # End Of File reached
            else:
                break # not matching event ends building the current result
        self.current_time_frame_begin = self.current_time_frame_end
        return result

    def read_next_event(self):
        line = self.source.readline().strip()
        if line:
            return line.split("::", maxsplit=2)
        return None

    def event_time(self):
        return float(self.current_event[0])
        
    def event_name(self):
        return self.current_event[1]

    def event_data(self):
        return self.current_event[2]
    

@dataclass(frozen=True)
class Event:
    time: float
    name: str
    data: str

    def __str__(self) -> str:
        return self.data


class EventSelector2:
    def __init__(self, source_file_path) -> None:
        source = open(source_file_path, "r")
        self.events = []
        for line in source.readlines():
            parts = line.strip().split("::", maxsplit=2)
            if len(parts) == 3:
                self.events.append(Event(float(parts[0]), parts[1], parts[2]))

    def select(self, time_beg, time_end, filter_in=None):
        result = list()
        if time_beg > self.events[-1].time:
            return None
        for event in self.events:
            if time_beg <= event.time and event.time < time_end:
                if filter_in and event.name not in filter_in:
                    continue
                result.append(event)
        return result
    
    def select_data(self, time_beg, time_end, filter_in=None):
        selection = self.select(time_beg=time_beg, time_end=time_end, filter_in=filter_in)
        if selection:
            result = ""
            for event in selection:
                if event.name == "STOP GAP7":
                    result += ' '
                else:
                    result += event.data
            return result
        return None


def main():
    from pprint import pprint
    es = EventSelector2("media\\audio\\out2.txt")
    result = es.select(0.1, 0.8, ["EXIT GROUP", "STOP GAP7"])
    pprint(result)
    text = es.select_data(0.1, 0.8, ["EXIT GROUP", "STOP GAP7"])
    print(text)

if __name__ == "__main__":
    main()
