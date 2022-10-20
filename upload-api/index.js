const express = require('express');
const multer = require('multer');
const matlab = require('node-matlab');
const app = express();



const fileFilter = function(req, file, cb) {
    const allowedTypes = ["text/csv"];

    if (!allowedTypes.includes(file.mimetype)) {
        const error = new Error("Wrong file type");
        error.code = "LIMIT_FILE_TYPES";
        return cb(error, false);
    }

    cb(null, true);
}




const MAX_SIZE = 200000;
const uploadMG = multer({
    dest: "./uploads-MG/",
    fileFilter,

    limits: {
        fileSize: MAX_SIZE
    }
});



const uploadEHR = multer({
    dest: "./uploads-EHR/",
    fileFilter,

    limits: {
        fileSize: MAX_SIZE
    }
});



app.post("/upload-MG", uploadMG.single("MG"), (req, res) => {
    res.json({ file: req.file, matlab: matlab.run("Hello.m").then((result) => console.log(result)).catch((error) => console.log(error)) })
}); 

app.post("/upload-EHR", uploadEHR.single("EHR"), (req, res) => {
    res.json({ file: req.file, matlab: matlab.run("Hello.m").then((result) => console.log(result)).catch((error) => console.log(error)) })
}); 


app.set('title', 'PredictMod')

app.use(function(err, req, res, next) {
    if (err.code === "LIMIT_FILE_TYPES") {
        res.status(422).json({ error: "Only .csv files are allowed"});
        return;
    }

    if (err.code === "LIMIT_FILE_SIZE") {
        res.status(422).json({ error: `Too large. Max size is ${MAX_SIZE / 1000}Kb`});
    }
})




app.listen(3344, () => console.log("Running on localhost:3344"));


