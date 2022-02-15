package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
)

func main() {

	postBody, _ := json.Marshal(map[string]string{
		"base_url": "https://facebook.com",
		"depth":    "2",
	})

	responseBody := bytes.NewBuffer(postBody)

	response, err := http.Post("http://127.0.0.1:8080/crawler/", "application/json", responseBody)
	fmt.Printf("This should not take more than 120 seconds or 2 minutes to get the site map \n")
	fmt.Printf("fetching links....\n")
	if err != nil {
		log.Fatal("An Error Occured: ", err)
	}
	if response.StatusCode == 200 || response.StatusCode == 201 {
		body, _ := ioutil.ReadAll(response.Body)
		fmt.Printf(strings.Replace(string(body), `\n`, "\n", -1))
	} else {
		fmt.Println("Http ResponseStatus: ", response.StatusCode)
	}
}
