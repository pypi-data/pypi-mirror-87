class ExactDelayPathfinder:
    def __init__(self):
        self._paths = []
        self._graph = None
        self._max_results = 0
        
        # Sets the limit of how many times a node can be visited when an edge
        # is traversed. Can be changed but not recommended to go above 1
        self._visit_limit = 1

    def search(self, graph, total_delay, start, end, max_results=10):
        """ Obtain paths with total delays equal or close to the user's requirements.
           If you want more or less results, you can change the value of the 
           result_count parameter value in the function signature

           Parameters:
              graph: a networkx graph object
              total_delay: the delay requirement for the result of the exact or closest path traversed
              start: The starting node for the path
              end: The end node for the path
              max_results : the number of results returned from the search (default is 10)
        """

        if graph is None:
            raise AttributeError("The graph must not be NoneType.")

        if max_results < 0:
            raise AttributeError("The result count limit must be a non-negative integer.")
        if total_delay < 0:
            raise AttributeError("The desired propagation delay must be a non-negative integer.")

        self._paths = []
        self._graph = graph
        self._max_results = max_results

        # This list prevents excessive cycling in the pathfinding process
        visits = {}

        for node in self._graph.nodes:
            visits[str(node)] = 0

        # Find paths that have delays close to the requested delay. The one in front of the list has
        # the closest matching delay of the lot.
        self._search(total_delay, start, end, [], visits)

        # Format result to list each path along with their total delays
        result = []

        for path in self._paths:
            result.append({"path":path["path"], "total_delay": total_delay - path["offset"]})

        return result

    def _search(self, delay, curr, target, path, visits):
        if (curr == target and path != []):
            error = abs(delay) # The target was reached
            if not bool(self._paths) or error < self._paths[0]["error"]:
                # The path is the node itself
                path.append(curr)
                # The path in front is the one with the lowest error
                self._paths.insert(0, {"path":path.copy(), "error":error, "offset":delay})
                # Clean up after the target was reached
                del path[-1]
                # Ensure that the list is at most the specified number elements in length (default is 10)
                if len(self._paths) > self._max_results:
                    del self._paths[-1]
            return
        path.append(curr) # Found a potential path with this as the starting node
        visits[str(curr)] += 1

        for neighbor in list(self._graph.neighbors(curr)):
            if (visits[str(neighbor)] < self._visit_limit):
                edge_delay = self._graph.edges[curr, neighbor]['delay']
                self._search(delay - edge_delay, neighbor, target, path, visits)

        del path[-1] # Clean up after a dead end was reached
        visits[str(curr)] -= 1
