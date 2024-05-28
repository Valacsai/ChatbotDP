import React from "react";
import ReactLoading from "react-loading";

export const isLoading = (loading, component) =>
  loading ? <Loading /> : component;

const Loading = ({text}) => {
  return (
    <>
        <ReactLoading
        type={"bubbles"}
        color={"#222232"}
        height={"20%"}
        width={"20%"}
        className="loading"
        />
        {text && <div>{text}</div>}
    </>
  );
};

export default Loading;