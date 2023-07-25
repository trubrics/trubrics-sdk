import React, {useEffect, useState} from "react";
import {init, save} from "./lib/firestore"
import Button from "@mui/material/Button";
import ThumbDownOffAltIcon from '@mui/icons-material/ThumbDownOffAlt';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from '@mui/material/TextField';


import './App.css';

const trubricsEmail = process.env.REACT_APP_TRUBRICS_EMAIL
const trubricsPassword = process.env.REACT_APP_TRUBRICS_PASSWORD

function App() {
  const [thumbScore, setThumbScore] = useState(null);
  const [open, setOpen] = useState(false);
  const [text, setText] = useState("");
  const [submit, setSubmit] = useState(false);
  useEffect(() => {
    if (open) {
      save(trubricsEmail, thumbScore === "up" ? "👍" : "👎", text, "react_test");
      setOpen(false)
      setSubmit(false)
      setText("")
      console.log("Feedback saved.")
    }
  }, [submit]);

  useEffect(() => {
    init(trubricsEmail, trubricsPassword)
  }, [trubricsEmail, trubricsPassword])

  const handleThumbClick = (score) => {
    setThumbScore(score);
    handleClickOpen();
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmitFeedback = () => {
    setSubmit(true);
  }
  return (
    <div className="App">
      <header className="App-header">
        {/* <p>Trubrics feedback components</p> */}
        <div id="thumbs-buttons">
          <ThumbUpOffAltIcon
            color="grey"
            sx={{
              px: 1,
              '&:hover': {
              cursor: 'pointer',
              color: 'green',
            }, }}
            onClick={() => handleThumbClick("up")}
            />
          <ThumbDownOffAltIcon
            color="grey"
            sx={{
              px: 1,
              '&:hover': {
              cursor: 'pointer',
              color: 'red',
            }, }}
            onClick={() => handleThumbClick("down")}
          />
        </div>
      </header>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
        fullWidth={true}
      >
        <DialogTitle id="alert-dialog-title">
          {thumbScore === "up" ? "👍 Provide additional feedback" : "👎 Provide additional feedback"}
        </DialogTitle>
        <DialogContent>
          <TextField
            id="outlined-textarea"
            label="What was the issue with the response? How could it be improved?"
            multiline
            rows={4}
            variant="filled"
            fullWidth={true}
            value={text}
            onChange={(event) => {
              setText(event.target.value);
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button sx={{color: "gray"}} onClick={handleClose}>Close</Button>
          <Button sx={{color: "gray"}} onClick={handleSubmitFeedback}>Submit feedback</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default App;
