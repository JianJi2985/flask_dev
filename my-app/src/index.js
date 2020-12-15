import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

// class Square extends React.Component {
//     // constructor(props){
//     //     super(props);
//     //     this.state={
//     //         value:null,
//     //     };
//     // }
//     render() {
//         return (
//             <button className="square" onClick={()=>this.props.onClick()}>
//                 {this.props.value}
//             </button>
//         );
//     }
// }
function Square(props) {
    return (
        <button className="square" onClick={props.onClick}>
            {props.value}
        </button>
    )
}

class Board extends React.Component {
    // handleClick(i) {
    //     const winner = calculateWinner(this.props.squares)
    //     const squares = this.props.squares.slice();
    //     if (winner || squares[i]) {
    //         return
    //     }
    //     squares[i] = this.props.xisnext ? 'X' : 'O'
    //     this.setState({squares: squares, xisnext: !this.props.xisnext})
    // }

    renderSquare(i) {
        return (<Square
                value={this.props.squares[i]}
                onClick={() => this.props.onClick(i)}
            />
        );
    }

    render() {
        // const winner = calculateWinner(this.props.squares);
        // let status
        // if (winner) {
        //     status = 'Winner ' + winner
        // } else {
        //     status = 'Next player: ' + (this.props.xisnext ? 'X' : 'O');
        // }

        return (
            <div>
                {/*<div className="status">{status}</div>*/}
                <div className="board-row">
                    {this.renderSquare(0)}
                    {this.renderSquare(1)}
                    {this.renderSquare(2)}
                </div>
                <div className="board-row">
                    {this.renderSquare(3)}
                    {this.renderSquare(4)}
                    {this.renderSquare(5)}
                </div>
                <div className="board-row">
                    {this.renderSquare(6)}
                    {this.renderSquare(7)}
                    {this.renderSquare(8)}
                </div>
            </div>
        );
    }
}


class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            history: [
                {squares: Array(9).fill(null),}
            ],
            xisnext: true,
            stepNumber: 0,
        }
    }

    jumpto(step) {
        this.setState({stepNumber: step, xisnext: (step % 2) === 0,})
    }

    handleClick(i) {
        const history = this.state.history.slice(0, this.state.stepNumber + 1)
        const current = history[history.length - 1]
        const winner = calculateWinner(current.squares)
        const squares = current.squares.slice();
        if (winner || squares[i]) {
            return
        }
        squares[i] = this.state.xisnext ? 'X' : 'O'
        this.setState({
            history: history.concat([{squares: squares}]),
            xisnext: !this.state.xisnext,
            stepNumber: history.length
        })
    }

    render() {
        const history = this.state.history.slice()
        const current = history[this.state.stepNumber]
        const winner = calculateWinner(current.squares)
        let status
        const moves = history.map(
            (step, move) => {
                const desc = move ? ('Go to move ' + move) : ('Go to the start')
                return (
                    <li key={move}>
                        <button onClick={() => this.jumpto(move)}>
                            {desc}
                        </button>
                    </li>
                )
            }
        )
        if (winner) {
            status = 'Winner is ' + winner
        } else {
            status = 'Next player is ' + (this.state.xisnext ? 'X' : 'O')
        }
        return (
            <div className="game">
                <div className="game-board">
                    <Board squares={current.squares} onClick={(i) => this.handleClick(i)}/>
                </div>
                <div className="game-info">
                    <div>{status}</div>
                    <ol>{moves}</ol>
                </div>
            </div>
        );
    }
}

function calculateWinner(squares) {
    const lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ];
    for (let i = 0; i < lines.length; i++) {
        const [a, b, c] = lines[i];
        if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
            return squares[a];
        }
    }
    return null;
}

// ========================================

ReactDOM.render(
    <Game/>,
    document.getElementById('root')
);
