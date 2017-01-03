Specifically, it obtains trains for the Red, Orange, and Blue Lines. The interface uses a <code>Station</code> class to obtain station attributes from the <code>RealTimeHeavyRailKeys.csv</code> file. 

The <code>next_trains</code> method returns a list of incoming trains. Each element in the list contains information about the train, in the order of: Line, Direction, Type (Predicted to Arrive or Arriving), Time of Arrival, Time Until Arrival. 

