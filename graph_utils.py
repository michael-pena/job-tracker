import plotly.graph_objects as go
from repository import ApplicationRepository

def generate_graph(repository: ApplicationRepository):
    total_applied = repository.get_count()
    rejected = repository.get_count_by_status('rejected')
    no_response = repository.get_count_by_status('no response')
    interviews = repository.get_count_by_status('interview')
    no_offer = repository.get_count_by_offer('no')
    yes_offer = repository.get_count_by_offer('yes')
    yes_accepted = repository.get_count_by_accepted('yes')
    no_accepted = repository.get_count_by_accepted('no')

    applied_node = 0
    rejected_node = 1
    no_response_node = 2
    interview_node = 3
    yes_offer_node = 4
    no_offer_node = 5
    yes_accepted_node = 6
    no_accepted_node = 7

    fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(
                pad=30,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[
                    "Total Applications: " + str(total_applied),
                    "Rejected: " + str(rejected),
                    "No Response: " + str(no_response),
                    "Interviews: " + str(interviews), 
                    "Offers: " + str(yes_offer),
                    "No Offer: " + str(no_offer),
                    "Accepted: " + str(yes_accepted),
                    "Declined: " + str(no_accepted)
                ],
            ),
            link=dict(
                # flow source node index
                source=[applied_node, applied_node, applied_node, interview_node, interview_node, yes_offer_node, yes_offer_node],
                # flow target node index
                target=[rejected_node, no_response_node, interview_node, yes_offer_node, no_offer_node, yes_accepted_node, no_accepted_node],
                # flow quantity for each source/target pair
                value=[rejected, no_response, interviews, yes_offer, no_offer, yes_accepted, no_accepted],
                ),
            )
        ]
    )

    fig.update_layout(width=900, height=450)
    return fig