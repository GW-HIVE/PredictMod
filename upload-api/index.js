const express = require('express');
const multer = require('multer');
const matlab = require('node-matlab');
const app = express();
const path = require('path')


const fileFilter = function(req, file, cb) {
    const allowedTypes = ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];

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
    res.json({ file: req.file})
}); 

app.post("/upload-EHR", uploadEHR.single("EHR"), (req, res) => {
    res.json({ file: req.file})
}); 



app.get('/output-EHR', function(req, res) {
    res.sendFile(path.join(__dirname, '/output-EHR/output.json'));
    });

app.get('/output-MG', function(req, res) {
    res.sendFile(path.join(__dirname, '/output-MG/output.json'));   
    });

app.get('/example-MG', function(req, res) {
    res.sendFile(path.join(__dirname, '/uploads-MG/example_MG_data.csv'));   
    });

app.get('/example-EHR', function(req, res) {
    res.sendFile(path.join(__dirname, '/uploads-EHR/example_EHR_data.xls'));   
    });
app.set('title', 'PredictMod')

app.use(function(err, req, res, next) {
    if (err.code === "LIMIT_FILE_TYPES") {
        res.status(422).json({ error: "Only .csv, .xls, and .xlsx files are allowed"});
        return;
    }

    if (err.code === "LIMIT_FILE_SIZE") {
        res.status(422).json({ error: `Too large. Max size is ${MAX_SIZE / 1000}Kb`});
    }
})




app.listen(3344, () => console.log("Running on localhost:3344"));


