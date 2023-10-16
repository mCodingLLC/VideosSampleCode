import sys

def my_trace_call(code, instruction_offset, call, arg0):
    print("Event: call")

def my_trace_line(code, line_number):
    print("Event: line")

def setup_monitoring():
    mo = sys.monitoring
    events = mo.events
    mo.use_tool_id(0, "my_debugger")
    mo.set_events(0, events.CALL | events.LINE)
    mo.register_callback(0, events.CALL, my_trace_call)
    mo.register_callback(0, events.LINE, my_trace_line)

def main():
    for x in range(5):
        print(x)

if __name__ == "__main__":
    setup_monitoring()
    main()

