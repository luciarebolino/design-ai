# 85-lr3102
import Rhino.Geometry as rh

class Agent:

    def __init__(self, pt, r, name, adjcs):

        self.cp = pt
        self.radius = r
        self.neighbors = []
        self.name = name
        self.adjacency = adjcs

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):

        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
    def collide(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d < self.radius + other.radius:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (self.radius + other.radius - d) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move other object
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

            # reverse vector and move self same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

        return amount

    # method for checking distance to other instance and moving closer if they are not touching
    def cluster(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d > self.radius + other.radius:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (d - (self.radius + other.radius)) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move self
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

            # reverse vector and move other object same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

        return amount

    def get_circle(self, plane):
        #return rh.Circle(self.cp, self.radius)
        return rh.Rectangle3d(plane, self.radius, self.radius)


def run(pts, radii, names, adjacencies, max_iters, alpha):

    print(adjacencies)
    print(names)

    agents = []

    for i, pt in enumerate(pts):

        print(names[i])

        my_agent = Agent(pt, radii[i], names[i], adjacencies[names[i]])
        agents.append(my_agent)

        print(names[i])
        
    #for each agent add all adjacency agents as its neighbor
    for i in range(len(agents)):
        
        for j in range(len(agents)):

            if agents[j].name in agents[i].adjacency:
                agents[i].add_neighbor(agents[j])
            else:
                continue

    for i in range(max_iters):

        total_amount = 0

        for j, agent_1 in enumerate(agents):

            # cluster to all agent's neighbors
            for agent_2 in agent_1.neighbors:
                total_amount += agent_1.cluster(agent_2, alpha)

            # collide with all agents after agent in list
            for agent_2 in agents[j+1:]:
                # add extra multiplier to decrease effect of cluster (change)
                total_amount += agent_1.collide(agent_2, alpha/4)

        if total_amount < .01:
            break

    iters = i

    circles = []

    # append circles in Rhino
    for agent in agents:
        circles.append(agent.get_circle())

    return circles, iters