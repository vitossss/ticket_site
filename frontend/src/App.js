import './App.css';
import Header from "./components/Header/Header";
import { ThemeProvider } from "@mui/material/styles"
import theme from "./components/styles/styles"
import PreHeader from "./components/Header/PreHeader";

function App() {

    return (
        <ThemeProvider theme={theme}>
            <div className="App">
                <PreHeader />
                <Header />
            </div>
        </ThemeProvider>
    );
}

export default App;
