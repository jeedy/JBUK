# React(리액트)
tags: front end, framwork

**React와** **babel, webpack**의 관계를 생각해보면 React는 그냥 **라이브러리**라고 생각되고 **babel**은 마치 **javac** 와 같은 **빌드툴(build tool)**로 느껴진다. **webpack**은 여러파일을 하나의 파일로 압축하는 **tool** 인것 같다. 

## 참고자료
1. [https://ko.reactjs.org/docs/hello-world.html](https://ko.reactjs.org/docs/hello-world.html) 리엑트 문서 및 API (Prototyping)
1. [https://babeljs.io/setup.html#installation](https://babeljs.io/setup.html#installation) babel 사용방법
1. [https://velopert.com/775 ](https://velopert.com/775) 리액트 사용법에 대해 자세히 설명되어있음.
1. [https://velopert.com/867](https://velopert.com/867) JSX 사용방법에 대해 잘 설명되어있음
1. [https://babeljs.io/repl/](https://babeljs.io/repl/) babel가 react 코드로 compiled 어떻게 시키는지 확인 할 수 있는 사이트
1. [https://velog.io/@velopert/react-redux-hooks] React hooks 사용법
1. [https://nikgraf.github.io/react-hooks/](https://nikgraf.github.io/react-hooks/) React Hooks 을 이용한 다양한 라이브러리
1. [https://github.com/rehooks/awesome-react-hooks](https://github.com/rehooks/awesome-react-hooks) React Hooks 을 이용한 다양한 라이브러리2

## 샘플소스
1. [html inline 샘플코드](./sample/index.html)
2. [리액트 샘플 코드(영화소개 프로젝트)]()
  참고자료 [https://ljh86029926.gitbook.io/coding-apple-react/before-start-class](https://ljh86029926.gitbook.io/coding-apple-react/before-start-class)



## 번외 (그냥 참고만하자)
ES6의 문법이 무엇인지, JSX가 무엇인지 알기 위해 참고용으로 소스를 정리한다. 실무에선 저렇게 쓸일은 없다. 최소한 **babel**를 이용하면 JSX와 ES6+ 문법을 모두 사용할 수 있다.



### 1. JSX 사용하지 않고 React를 사용하는 방법
참고자료:
- [https://reactjs.org/docs/react-without-jsx.html](https://reactjs.org/docs/react-without-jsx.html)

JSX 사용할 경우 :
```javascript
class Hello extends React.Component {
  render() {
    return <div>Hello {this.props.toWhat}</div>;
  }
}

ReactDOM.render(
  <Hello toWhat="World" />,
  document.getElementById('root')
);
```

JSX 사용하지 않은 경우: 
```javascript
class Hello extends React.Component {
    render() {
        // 직접 메소드를 호출해서 구현해야한다.
        return React.createElement('div', null, `Hello ${this.props.toWhat}`); 
    }
}

ReactDOM.render(
    React.createElement(Hello, {toWhat: 'World'}, null),
    document.getElementById('root')
);
```


### 2. ES6 사용하지 않고 React를 사용하는 방법

참고자료: 
- [https://reactjs.org/docs/react-without-es6.html](https://reactjs.org/docs/react-without-es6.html)

ES6+ 문법을 사용하려고 할 때 :
```javascript
// ES6+
class SayHello extends React.Componet {
    constructor(props) {
        super(props);
        this.state = {message: props.msg};
        // This line is important!
        this.handleClick = this.handleClick.bind(this);
    }

  handleClick() {
    alert(this.state.message);
  }
  render() {
    // Because `this.handleClick` is bound, we can use it as an event handler.
    return (
      <button onClick={this.handleClick}>
        Say hello
      </button>
    );
  }
}

SayHello.defaultProps = {
  name: 'Mary'
};
```

ES6이하 문법을 사용하려고 할 때:
```javascript
var SayHello = createReactClass({
    getDefaultProps: function() {       // SayHello.defaultProps 선언대신
        return {
            name: 'Mary'
        };
    },

    getInitialState: function() {     // constructor() 대신 getInitialState()에 구현
        return {message: this.props.msg};
    },

    handleClick: function() {         // handleClick()
        alert(this.state.message);
    },

    render: function() {              // render()
        return (
            <button onClick={this.handleClick}>
                Say hello
            </button>
        );
    }
});
```


