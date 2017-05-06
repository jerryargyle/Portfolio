module Main exposing (..)
import Html.Attributes exposing (..)
import Html exposing (..)
import Html.Events exposing (onClick)

stylesheet =
    let
        tag = "link"
        attrs =
            [ attribute "rel"       "stylesheet"
            , attribute "property"  "stylesheet"
            , attribute "href"      "./style.css"
            ]
        children = []
    in
        node tag attrs children
main =
  Html.program
  { init = createModel
  , view = view
  , update = update
  , subscriptions = \_ -> Sub.none
  }


type Group =
  Image
  | Text

type Msg =
    Select Model

helper : String -> Html Msg
helper name =
  div [(class "container")] [stylesheet
                            , img [ (class "alignment"), (height 750), (width 750) ,(src name), (attribute "usemap" "#imagemap")] []
                            , node "map" [attribute "name" "#imagemap"]
                                            [ areaHelper "0, 0, 250, 250" Frontal
                                              , areaHelper "250, 0, 500, 200" Parietal
                                              , areaHelper "100 ,250 ,500 ,380  " Temporal
                                              , areaHelper "580, 270, 700, 350" Occipital
                                              , areaHelper "300, 380, 550, 500" Cerebellum
                                            ]
                            , button [onClick (Select First)] [text "Back to the Brain!"]
                            ]
areaHelper : String -> Model -> Html Msg
areaHelper coords model =
   node "area"
      [ attribute "shape" "rect"
        , attribute "coords" coords
        ,  onClick (Select model)
      ] []


--View
view : Model -> Html Msg
view model =
          case model of
            First ->
              (helper "./images/Brain.png")          --  div [] [ stylesheet , (div [ class "wrapper" ] (List.map showLobe brain) ) ]\
            Occipital ->
              (helper "./images/OccipitalWords.png")
            Temporal ->
              (helper "./images/TemporalWords.png")
            Frontal ->
              (helper "./images/FrontalWords.png")
            Cerebellum ->
              (helper "./images/CerebellumWords.png")
            Parietal ->
              (helper "./images/ParietalWords.png")

type Model =
          First
          | Occipital
          | Parietal
          | Temporal
          | Cerebellum
          | Frontal

createModel : ( Model, Cmd Msg )
createModel =
            (First, Cmd.none)

update : Msg -> Model -> ( Model, Cmd Msg )
update (Select newModel) model = (newModel, Cmd.none)
