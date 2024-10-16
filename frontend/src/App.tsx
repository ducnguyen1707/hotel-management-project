import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "react-router-dom";
import Home from "./pages/Home";

const router = createBrowserRouter(
    createRoutesFromElements(
      <Route>
        <Route path="/hello" element={<Home />}/>
      </Route>
    )
);
const App = () => {
  return <RouterProvider router={router} /> ;
};
export default App
