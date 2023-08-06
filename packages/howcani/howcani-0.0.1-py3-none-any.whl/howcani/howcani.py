import argparse

from howcani.plugins import StackOverflowPlugin
from howcani.plugins.stackoverflow import TYPE_STACKOVERFLOW 

def main():
    '''
    Main Method.
    '''
    parser = argparse.ArgumentParser(prog='howcani', description="Command Line Utility to search for basic programming related queries.")

    # Search Query Parameter
    parser.add_argument(
        'query',
        metavar='q',
        type=str,
        help='Query String to Search.',
        nargs='+'
    )

    # Number of Answers to be returned.
    parser.add_argument(
        '--count',
        type=int,
        help='Number of Search Results to be entered.',
        default=1,
        nargs='?'
    )

    # Number of Answers to be returned.
    parser.add_argument(
        '--plugin',
        type=str,
        help='Plugin to use: stackoverflow(s/default)',
        default="stackoverflow",
        nargs='?'
    )

    args = parser.parse_args()

    query_str = ' '.join(args.query)
    num_answers = args.count
    plugin = args.plugin

    answers = []

    if plugin == TYPE_STACKOVERFLOW:
        stackoverflow = StackOverflowPlugin()
        answers = stackoverflow.get_results(query=query_str, n=num_answers)
        
    
    if len(answers) == 0:
        print(":( No Results Found...")
    else:
        for i in range(num_answers):
            print("--------------------------------")
            print(answers[i])
            print("--------------------------------")
    

