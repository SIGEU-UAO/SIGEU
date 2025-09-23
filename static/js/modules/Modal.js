export default class Modal{
    static closeModal(modal){
        modal.close()
    }

    static toggleResultsVisibility(result){
        result.classList.toggle("hide")
    }
}